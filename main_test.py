from datetime import datetime
from inspect import trace
import traceback, json, os, github

#==============================

def find_repo (api: github.Github, name: str) -> github.Repository:
    for repo in api.get_repos ():
        if repo.full_name == name: return repo

    return None

#==============================

def list_repo (repo) -> list[str]:
    files = []

    contents = repo.get_contents ("")
    while contents:
        file_content = contents.pop (0)

        if file_content.type == 'dir':
            contents.extend (repo.get_contents (file_content.path))
            continue

        files.append (file_content.path)

    return files

#==============================

def list_dir (root: str) -> list[str]:
    if not len (root):
        root = '.'

    files = []

    def recursive (path: str):
        contents = os.listdir (path)

        while contents:
            filename = path + '/' + contents.pop (0)

            if os.path.isdir (filename):
                recursive (filename)
                continue

            files.append (filename[2:])

    recursive (root)
    return files

#==============================

def sync_repo (repo: github.Repository, dir_path: dict):
    repo_list = list_repo (repo)
    dir_list  = list_dir  (dir_path)

    elements = []
    encoding = "utf-8"

    commit_title = datetime.strftime (datetime.now (), "Auto commit at [%H:%M:%S]")

    for filename in dir_list:
        with open ('./' + filename, mode = 'r', encoding = encoding) as file:
            file_contents = file.read ()
            file.close ()

        blob = repo.create_git_blob (file_contents, encoding)
        elements.append (github.InputGitTreeElement (path = filename, mode = '100644', type = 'blob', sha = blob.sha))


        #if not filename in repo_list:
        #    print (f"Creating file '{filename}'")
        #    repo.create_file (filename, commit_title, file_contents)
            
        #else: 
        #    print (f"Updating file '{filename}'")
        #    contents = repo.get_contents (filename)
        #    repo.update_file (filename, commit_title, file_contents, contents.sha)

    head_sha   = repo.get_branch        ('master').commit.sha
    base_tree  = repo.get_git_tree      (sha = head_sha)
    tree       = repo.create_git_tree   (elements, base_tree)
    parent     = repo.get_git_commit    (sha = head_sha)
    commit     = repo.create_git_commit (commit_title, tree, [parent])
    master_ref = repo.get_git_refs      ()[0]

    master_ref.edit (sha = commit.sha)

    #for filename in repo_list:
    #    if not filename in dir_list:
    #        print (f"Deleting file '{filename}'")
    #        contents = repo.get_contents (filename)
    #        repo.delete_file (filename, commit_title, contents.sha)

#==============================

def main ():
    print ("Enter token: ", end = "")
    api = github.Github (input ())
    me = api.get_user ()

    repo = find_repo (me, "Smok1e/test-auto-commit")
    if not repo:
        raise RuntimeError ("Failed to find a repository")

    sync_repo (repo, "")

#==============================

try: main ()
except Exception as exc:
    print (f"\n\nUnhandled exception: {exc}")

    with open ("exception.txt", 'w') as file:
        file.write (traceback.format_exc ())
        file.close ()

#==============================