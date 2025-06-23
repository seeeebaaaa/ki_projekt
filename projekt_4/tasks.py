# from projekt_4.app import celery_app
import pygit2
import shutil
import requests
from time import sleep
from random import random
from pathlib import Path
from celery import shared_task, current_task, group, chord

from projekt_4.config import create_app  # -Line 1
from projekt_4.redis_helper import save_progress, get_progress
from parser import python_to_ast_json, python_parse_file, build_docu
import subprocess
from sp_docs import sphinx_gen_docs  
flask_app = create_app()  # -Line 2
celery_app = flask_app.extensions["celery"]  # -Line 3


# @shared_task(ignore_result=False)
# def start_process(session_id):
#     for i in range(1, 11):  # Simulate a 10-step task
#         sleep(i / 4)
#         current_task.update_state(
#             state="PROGRESS", meta={"progress": i / 10, "session_id": session_id}
#         )
#     current_task.update_state(
#         state="SUCCESS", meta={"endergebnis": "Task Completed Successfully!"}
#     )


class GitProgressCallback(pygit2.RemoteCallbacks):

    def __init__(self, uid, credentials=None, certificate_check=None):
        super().__init__(credentials, certificate_check)
        self.uid = uid

    def transfer_progress(self, stats):
        save_progress(
            self.uid, {"state_status": f"{stats.indexed_objects}/{stats.total_objects}"}
        )


@shared_task(ignore_result=False)
def start_clone_git(session_id):
    """Clone the given git into the data volume under the uid and provide file structure"""
    save_progress(
        session_id,
        {
            "task_state": "started",
            "state_text": "Accessing Repo..",
            "state_status": "0/???",
        },
    )  # git link
    git_link = get_progress(session_id)["git_link"]
    # user path
    user_path: Path = Path("/data") / session_id
    # remove folder if it already exists
    if user_path.exists() and user_path.is_dir():
        shutil.rmtree(user_path)
    # make sure the path exits
    user_path.mkdir(exist_ok=True)
    # clone the repo (callback updates progress)
    repo = pygit2.clone_repository(
        url=git_link, path=user_path, callbacks=GitProgressCallback(session_id)
    )
    remote_branches = [
        b.lstrip("origin/") for b in repo.branches.remote
    ]  # remove origin prefix for visibility
    # get files for frontend
    files = [
        str(p)[len("/data/" + session_id + "/") :] for p in user_path.glob("**/**")
    ]
    files.remove("")  # remove base path
    # Remove every path that is /.git/*
    files = [
        f
        for f in files
        if not f.startswith(".git/") and "/.git/" not in f and f != ".git"
    ]
    print(files)
    save_progress(
        session_id,
        {
            "data": {"branches": remote_branches, "files": files},
            "state": "select",
            "state_text": "",
            "state_status": "",
            "task_state": "done",
        },
    )
    current_task.update_state(state="SUCCESS")


@shared_task(ignore_result=False)
def select_switch_branch(session_id, branch_name):
    """Switch to another branch"""
    return {}


@shared_task(ignore_result=False)
def process_files(uid):
    """Acts as the starting point for parse&prompting tasks. Will filter out relevant paths and start everything"""
    info = get_progress(uid)
    files = info["files_to_process"]

    # this checks, if the files are where they are supposed to be, so the user cant get access to files via ../../ etc
    base_path = Path("/data") / uid
    files = [str(base_path) + f for f in files]
    valid_files = [
        Path(f)
        for f in files
        if base_path in Path(f).resolve().parents and Path(f).exists()
    ]
    print("Valid paths:", valid_files)
    print("All files:", files)
    if not valid_files:
        raise ValueError("No valid files to process.")
    # update state progress to match everything
    save_progress(
        uid,
        {
            "state": "ai",
            "state_text": f"Parsing files.. ({len(valid_files)})",
            "state_status": "",
        },
    )
    # Collects all paths and starts parsing group
    task_list = [ai_parse.s({"uid": uid, "file": str(file)}) for file in valid_files]
    return chord(task_list)(ai_prompt_group.s())


@shared_task(ignore_result=False)
def ai_parse(args):
    """Parses the given file (path) and returns result"""
    uid = args["uid"]
    file = Path(args["file"])
    ast_json = python_parse_file(file_path=str(file)) # maybe try again with ast2json package. ast.dump() is not working
    # update client progress
    save_progress(uid, {"state": "ai", "state_status": f"Parsed {file.name}"})
    return {"uid": uid, "file": str(file)}


@shared_task(ignore_result=False)
def ai_prompt_group(parsed_results):
    """Collects all parsing results and starts prompting group"""
    uid = parsed_results[0]["uid"]
    # update client progress
    save_progress(
        uid,
        {
            "state": "ai",
            "state_text": f"Prompting files.. ({len(parsed_results)})",
            "state_status": "",
        },
    )
    # kick of celery tasks
    task_list = [ai_prompt.s(result) for result in parsed_results]
    return chord(task_list)(collect_all_prompted.s())


@shared_task(ignore_result=False)
def ai_prompt(args):
    """Prompt AI for changes etc for one instance (this task is created for each change)"""
    uid = args["uid"]
    file = Path(args["file"])
    args["prompted"] = True
    print ("Prompting file:" + str(file))

    try:
        docstring_code = build_docu(file_path=str(file))
        # print("module Docstring code:", docstring_code)
        # Call the prompter microservice

        # Not working, failing to resole "parser"
        # prompter_response = requests.post(
        #     "http://parser:5000/docu",
        #     json={"file_path": str(file)},  # Pass serialized AST
        # )
        # prompter_response.raise_for_status()
        # api_docstring_code = prompter_response.json()[
        #     "docstring_code"
        # ]  # Get generated code with docstrings
        # print("api Docstring code:", api_docstring_code)
        
        args["prompt_result_file"] = docstring_code
    except Exception as e:
        args["prompt_result_file"] = f"Error: {str(e)}"

    save_progress(uid, {"state": "ai", "state_status": f"Prompted {file.name}"})
    return args


@shared_task(ignore_result=False)
def collect_all_prompted(prompt_results):
    """Collects all prompted results to return in one object/push to db and change status so client can update progress steps."""
    uid = prompt_results[0]["uid"]
    print("All prompts done:", prompt_results)
    # remove all /data/<uid>/ prefixes from files:
    base_path = f"/data/{uid}/"
    for result in prompt_results:
        if result["file"].startswith(base_path):
            result["file"] = result["file"][len(base_path) :]

    save_progress(
        uid,
        {
            "result": prompt_results,
            "state": "review",
            "state_text": "",
            "state_status": "",
            "task_state": "done",
        },
    )
    current_task.update_state(state="SUCCESS")
    return prompt_results


@shared_task(ignore_result=False)
def review_apply_changes(uid):
    """Apply the changes the reviewer made in a new branch of the local repo"""
    return {}


@shared_task(ignore_result=False)
def bundle_create_bundle(uid):
    """Create a git bundle, so the changed repository can be imported as a new branch."""
    info = get_progress(uid)
    file_changes:dict[str,str] = info["file_changes"]
    save_progress(
        uid,
        {
            "state": "bundle",
            "state_text": "Applying Changes..",
            "state_status": "",
        }
    )
    base_path = Path("/data") / uid
    for rel_path, content in file_changes.items():
        file_path = base_path / rel_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    # pause for progress update
    repo = pygit2.Repository(str(base_path))
    index = repo.index
    index.add_all()
    index.write()

    tree = index.write_tree()
    author = pygit2.Signature("Projekt 4", "changes@projekt_4.com")
    committer = author

    head_ref = repo.head.target
    commit = repo.create_commit(
        "refs/heads/changes",
        author,
        committer,
        "apply changes",
        tree,
        [head_ref]
    )

    # Bundle the "changes" branch
    bundle_path:Path = base_path / "changes.bundle"
    subprocess.run(
        ["git", "-C", str(base_path), "bundle", "create", str(bundle_path), "changes"],
        check=True
    )

    sleep(1)
    save_progress(
        uid,
        {
            "state": "bundle",
            "state_text": "Applied Changes",
            "state_status": "",
            "task_state": "done",
            "link_to_bundle": str(bundle_path.absolute())
        }
    )
    return {}

@shared_task(ignore_result=False)
def generate_docs(uid):
    """Generate Sphinx documentation for the repository"""
    base_path = Path(f"/data/{uid}/")
    # Check if the base path exists
    if not base_path.exists():
        raise FileNotFoundError(f"Base path {base_path} does not exist.")
    
    # Generate documentation
    try:
        sphinx_gen_docs(base_path)
        save_progress(uid, {"state": "docs", "state_text": "Documentation generated successfully."})
    except Exception as e:
        save_progress(uid, {"state": "docs", "state_text": f"Error generating documentation: {str(e)}"})
        raise e
    
    current_task.update_state(state="SUCCESS")