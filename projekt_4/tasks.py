# from projekt_4.app import celery_app
from projekt_4.config import create_app  # -Line 1
from celery import shared_task, current_task
from time import sleep
import pygit2
from pathlib import Path
import shutil
from projekt_4.redis_helper import save_progress, get_progress

flask_app = create_app()  # -Line 2
celery_app = flask_app.extensions["celery"]  # -Line 3


@shared_task(ignore_result=False)
def start_process(session_id):
    for i in range(1, 11):  # Simulate a 10-step task
        sleep(i / 4)
        current_task.update_state(
            state="PROGRESS", meta={"progress": i / 10, "session_id": session_id}
        )
    current_task.update_state(
        state="SUCCESS", meta={"endergebnis": "Task Completed Successfully!"}
    )


class GitProgressCallback(pygit2.RemoteCallbacks):

    def __init__(self, uid, credentials=None, certificate_check=None):
        super().__init__(credentials, certificate_check)
        self.uid = uid

    def transfer_progress(self, stats):
        save_progress(self.uid,{"state_status":f'{stats.indexed_objects}/{stats.total_objects}'})

@shared_task(ignore_result=False)
def start_clone_git(session_id):
    """Clone the given git into the data volume under the uid and provide file structure"""
    save_progress(session_id,{"task_state":"started","state_text":"Cloning Repo.."})# git link
    git_link = get_progress(session_id)["git_link"]
    # user path
    user_path: Path = Path("/data") / session_id
    # remove folder if it already exists
    if user_path.exists() and user_path.is_dir():
        shutil.rmtree(user_path)
    # make sure the path exits
    user_path.mkdir(exist_ok=True)
    # clone the repo (callback updates progress)
    repo = pygit2.clone_repository(url=git_link, path=user_path,callbacks=GitProgressCallback(session_id))
    remote_branches = [
        b.lstrip("origin/") for b in repo.branches.remote
    ]  # remove origin prefix for visibility
    # get files for frontend
    files = [str(p)[len("/data/"+session_id+"/"):] for p in user_path.glob("**/**")]
    files.remove("") # remove base path
    save_progress(session_id,{"data":{"branches":remote_branches,"files":files},"state":"select","state_text":"","state_status":"","task_state":"done"})
    current_task.update_state(state="SUCCESS")


@shared_task(ignore_result=False)
def select_switch_branch(session_id, branch_name):
    """Switch to another branch"""
    return {}


@shared_task(ignore_result=False)
def ai_parse(session_id):
    """Parse selected files"""
    return {}


@shared_task(ignore_result=False)
def ai_prompt(session_id):
    """Prompt AI for changes etc for one instance (this task is created for each change)"""
    return {}


@shared_task(ignore_result=False)
def review_apply_changes(session_id):
    """Apply the changes the reviewer made in a new branch of the local repo"""
    return {}


@shared_task(ignore_result=False)
def bundle_create_bundle(session_id):
    """Create a git bundle, so the changed repository can be imported as a new branch."""
    return {}
