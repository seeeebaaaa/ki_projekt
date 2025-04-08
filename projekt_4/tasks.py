# from projekt_4.app import celery_app
from projekt_4.config import create_app  # -Line 1
from celery import shared_task, current_task
from time import sleep

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

@shared_task(ignore_result=False)
def start_clone_git(session_id,git_link):
   """Clone the given git into the data volume and provide file structure"""
   return {}

@shared_task(ignore_result=False)
def select_switch_branch(session_id,branch_name):
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
   return {}

@shared_task(ignore_result=False)
def bundle_create_bundle(session_id):
   return {}