from flask import jsonify, request, render_template, session, redirect, url_for
from markupsafe import Markup
import os
import uuid
from functools import wraps
from celery.result import AsyncResult
import validators
from projekt_4.tasks import flask_app as app, start_process

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

# route to check if a task is done
@app.get("/progress")
@ensure_session
def progress() -> dict[str, object]:
    task_id = session.get("task_id")
    if not task_id:
        return jsonify({"error":"You dont have any running task!"})
    task = AsyncResult(task_id)
    print("="*5,task_id,task,task.info,"="*5,sep="\n")
    return jsonify(
        {
            "state":task.state,
            "ready": task.ready(),
            "successful": task.successful(),
            "value": task.result if task.ready() else None,
            "progress":task.info["progress"] if task.info and "progress" in task.info else None,
        }
    )

@app.post("/start")
@ensure_session
def start():
    print("S"*5,session.get("_id"),"S"*5,sep="\n")
    data = request.json
    git_link = data.get('git_link')
    if not validators.url(git_link):
        return jsonify({"error":"Not a valid url"})
    # create task
    result = start_process.apply_async(args=[session.get("_id")])
    print("*"*20,"Task Created under id:",result,"*"*20,sep="\n")
    session["task_id"] = result.id
    return jsonify({"success": "Task created"})


