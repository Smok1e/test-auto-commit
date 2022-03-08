from github   import Github, Repository
from datetime import datetime
import traceback, json, os

#==============================

def find_repo (api: Github, name: str) -> Repository:
    for repo in api.get_repos ():
        if repo.full_name == name: return repo

    return None

#==============================

def list_repo (repo):
    def recursive (dir, path: str):
        contents = repo.get_contents (path)

        while contents:
            current = contents.pop (0)

            if current.type == 'dir':
                dir[current.name] = {}
                recursive (dir[current.name], current.path)

                continue

            dir[current.name] = current.path

    root = {}
    recursive (root, "")

    return root

#==============================

def list_dir (path: str) -> dict:
    if not len (path):
        path = '.'

    def recursive (dir, path: str):
        contents = os.listdir (path)

        while contents:
            current = path + '/' + contents.pop (0)
            filename = os.path.split (current)[1]

            if os.path.isdir (current):
                dir [filename] = {}
                recursive (dir[filename], current)

                continue

            dir[filename] = current

    root = {}
    recursive (root, path)

    return root

#==============================

def sync_repo (repo, dir_path: dict):
    dir_contents  = list_dir  (dir_path)
    repo_contents = list_repo (repo)

    def recursive (repo: Repository, dir: dict):
        dir_keys  = list (dir_contents.keys  ())
        repo_keys = list (repo_contents.keys ())

        while dir_keys:
            current_dir_item = dir_contents[dir_keys.pop (0)]

            if isinstance (current_dir_item, dict):
                continue

            if not 

    def recursive (repo: Repository: dir: dict):
        keys = list (dir.keys ())

        while :
            contents = dir.pop (keys.pop (0))

            if isinstance (contents, dict):
                recursive (contents)

                continue
            
            path = contents[2:]
            with open (path) as file:
                file_contents = file.read ()
                file.close ()

            repo.create_file (contents[2:], datetime.strftime (datetime.now (), "Auto commit at [%H:%M:%S]"), file_contents)

    recursive (repo, dir_contents)

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