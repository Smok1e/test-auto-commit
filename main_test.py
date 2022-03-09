from github   import Github, Repository
from datetime import datetime
import traceback, json, os

#==============================

def find_repo (api: Github, name: str) -> Repository:
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

def sync_repo (repo: Repository, dir_path: dict):
    repo_list = list_repo (repo)
    dir_list  = list_dir  (dir_path)

    commit_title = datetime.strftime (datetime.now (), "Auto commit at [%H:%M:%S]")

    for filename in dir_list:
        with open ('./' + filename, 'r') as file:
            file_contents = file.read ()
            file.close ()

        if not filename in repo_list:
            print (f"Creating file '{filename}'")
            repo.create_file (filename, commit_title, file_contents)
            
        else: 
            print (f"Updating file '{filename}'")
            contents = repo.get_contents (filename)
            repo.update_file (filename, commit_title, file_contents, contents.sha)

    for filename in repo_list:
        if not filename in dir_list:
            print (f"Deleting file '{filename}'")
            contents = repo.get_contents (filename)
            repo.delete_file (filename, commit_title, contents.sha)

#==============================

def main ():
    api = Github ("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")
    me = api.get_user ()

    repo = find_repo (me, "Smok1e/test-auto-commit")
    if not repo:
        raise RuntimeError ("Failed to find a repository")

    sync_repo (repo, "")

#==============================

try: main ()
except Exception as exc:
    print ("\n")
    print (f"Unhandled exception: {exc}")
    print ("\n===============================\n")
    traceback.print_exc ()

#==============================