from importlib.metadata import requires
import requests, json, traceback, http.client

#==================================

def save_json (filename: str, data: dict) -> None:
    with open (filename, 'w') as file:
        json.dump (data, file, indent = 4)
        file.close ()

#==================================

def save_response (filename: str, response: requests.Response) -> None:
    if not response.headers['content-type'].find ('json'):
        raise RuntimeError ("Request is not json")

    save_json (filename, response.json ())

#==================================

def request (url: str, filename: str):
    response = requests.get ("https://api.github.com/repos/Smok1e/test-auto-commit/commits")
    save_response (filename, response)

    if (response.status_code != requests.codes.ok):
        print (f"Request failed: {http.client.responses[response.status_code]} ({response.status_code})")
        return None

    return response.json ()

#==================================

def main ():
    commits = request ("https://api.github.com/repos/Smok1e/test-auto-commit/commits", "request_commits.json")
    if not commits:
        return None

    tree = request (commits[0]['commit']['tree'], "response_tree.json")
    if not tree:
        return None

#==================================

try: main ()
except Exception as exc:
    print (f"\nUnhandled exception: {exc}"               )
    print (f"\n=========================================")
    print (f"\n{traceback.format_exc ()}"                )

#==================================