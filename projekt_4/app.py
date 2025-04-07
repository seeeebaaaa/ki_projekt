from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from markupsafe import Markup
from celery import Celery, Task, shared_task, current_task
from flask_session import Session
import requests
import os
from flask_talisman import Talisman
import uuid
from celery.result import AsyncResult
from time import sleep
from secrets import token_urlsafe
from functools import wraps
from flask_static_digest import FlaskStaticDigest

app = Flask(__name__,static_folder="../public",static_url_path="")
app.config.from_object("config.settings")
app.secret_key = token_urlsafe()
Session(app)
# Talisman(app) #breaks inline script, needs to be configured some how but idfk what
FlaskStaticDigest(app)

def init_celery_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config.get("CELERY_CONFIG",{}))
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

celery_app = init_celery_app(app)

# svg helper to render them inline
# Assuming SVGs are in 'static/svg/'
@app.context_processor
def utility_processor():
    def inline_svg(filename):
        svg_path = os.path.join(app.static_folder, 'svg', filename)
        try:
            with open(svg_path, 'r', encoding='utf-8') as f:
                return Markup(f.read())  # Markup prevents Jinja from escaping the content
        except FileNotFoundError:
            return f"<!-- SVG file '{filename}' not found -->"
    return dict(inline_svg=inline_svg)


def ensure_session(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # print("=" * 20)
        # print(session)
        if "_id" not in session:
            print("[ENSURE_SESSION] No ID set, assinging new id..")
            session["_id"] = uuid.uuid1()
            return redirect(url_for("home"))
        # print("=" * 20)
        return f(*args, **kwargs)

    return decorated

@app.route("/", methods=["GET"])
@ensure_session
def home():
    return render_template("index.html")


@app.route("/getLower", methods=["POST"])
@ensure_session
def get_lower_data():
    data = request.json
    code = data["code"]
    response = requests.post("http://ast:5000/toLower", json={"code": code})
    return jsonify(response.json())


@app.route("/startsampleprocess", methods=["GET"])
@ensure_session
def startsampleprocess():
    print("ayayayay"*10)
    result = sample_process.apply_async(args=[session.get("_id")])
    print("*"*20,result,"*"*20,sep="\n")
    return jsonify({"task_id": result.id})


# route to check if a task is done
@app.get("/task/<id>")
# @ensure_session
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
