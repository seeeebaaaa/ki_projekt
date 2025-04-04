from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from celery import Celery, Task, shared_task, current_task
from flask_session import Session
import requests
import os
from redis import Redis
from flask_talisman import Talisman
from turbo_flask import Turbo
import uuid
from celery.result import AsyncResult
from time import sleep
from secrets import token_urlsafe
from functools import wraps
import json

app = Flask(__name__)
SESSION_TYPE = "redis"
SESSION_REDIS = Redis(host=os.environ["REDIS_HOST"], port=os.environ["REDIS_PORT"])
app.config.from_object(__name__)
app.secret_key = token_urlsafe()
Session(app)
turbo = Turbo(app)
# Talisman(app) #breaks inline script, needs to be configured some how but idfk what

# import own modules and functions, after app is initalized


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


@turbo.user_id
def get_user_id():
    print(f"{'-'*10}\nRETURNED USER ID: {session['_id']}\n{'-'*10}")
    return session["_id"]


# def set_session():
#     if "_id" not in session:
#         # generate a new session id
#         session["_id"] = uuid.uuid1()


def ensure_session(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print("=" * 20)
        print(turbo.clients)
        print(session)
        if "_id" not in session:
            session["_id"] = uuid.uuid1()
        if session["_id"] not in turbo.clients and request.endpoint != "home":
            print(session["_id"], turbo.clients)
            print("=" * 20)
            return redirect(url_for("home"))
        print("=" * 20)
        return f(*args, **kwargs)

    return decorated


# set up celery
app.config.from_mapping(
    CELERY=dict(
        broker_url=os.environ["CELERY_BROKER_URL"],  # set via dockerfile
        result_backend=os.environ["CELERY_RESULT_BACKEND"],  # set via dockerfile
        task_ignore_result=True,
    ),
)

celery_app = init_app(app)


@app.route("/", methods=["GET"])
@ensure_session
def home():
    print(session)
    print(turbo.clients)
    print(turbo.can_push())
    print(turbo.can_stream())
    healthy = requests.get("http://ast:5000/healthy")
    return render_template("index.html", healthy=healthy.text)


@app.route("/getLower", methods=["POST"])
def get_lower_data():
    data = request.json
    code = data["code"]
    response = requests.post("http://ast:5000/toLower", json={"code": code})
    return jsonify(response.json())


@app.route("/startsampleprocess", methods=["GET"])
@ensure_session
def startsampleprocess():
    result = sample_process.apply_async(args=[session.get("_id")])
    return jsonify({"task_id": result.id})


# route to check if a task is done
@app.get("/task/<id>")
@ensure_session
def task_result(id: str) -> dict[str, object]:
    task = AsyncResult(id)
    return jsonify(
        {
            "state":task.state,
            "ready": task.ready(),
            "successful": task.successful(),
            "value": task.result if task.ready() else None,
            "progress":task.info["progress"] if task.info and "progress" in task.info else None,
        }
    )


@shared_task(ignore_result=False)
def sample_process(session_id):
    for i in range(1, 11):  # Simulate a 10-step task
        sleep(i/4)
        current_task.update_state(
            state="PROGRESS", meta={"progress": i / 10, "session_id": session_id}
        )
    current_task.update_state(
        state="SUCCESS", meta={"endergebnis": "Task Completed Successfully!"}
    )
