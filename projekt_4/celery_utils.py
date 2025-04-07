from celery import Celery, Task, shared_task
from flask import Flask
from time import sleep
import app as flask_app

def init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

# @shared_task(ignore_result=False,bind=True)
# def sample_process(self,session_id):
#     sum_ = 0
#     for i in range(10):
#         sleep(2)
#         print(f"Processing {i}")
#         sum_ += i
#         self.update_state(state="PROGRESS", meta={'progress': 90,"session_id":session_id})
#     return sum_

def push_progress(task_body):
    if "result" in task_body and "progress" in task_body["result"]:
        flask_app.turbo.push(flask_app.turbo.stream(flask_app.turbo.replace(f'<div class="progress" style="height:1em;width: {(task_body["result"]["progress"]/10)*10}em;background:red;"></div>', target="sample-progress-bar")),to=task_body["result"]["session_id"])