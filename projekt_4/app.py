from flask import jsonify, request, render_template, session, redirect, url_for, send_file
from markupsafe import Markup
import os
import uuid
from functools import wraps
from celery.result import AsyncResult
import validators
from projekt_4.tasks import flask_app as app, start_clone_git, process_files, bundle_create_bundle, generate_docs
from projekt_4.redis_helper import get_progress, init_progress, save_progress
from pathlib import Path
import shutil
import tempfile

# svg helper to render them inline
# Assuming SVGs are in 'static/svg/'
@app.context_processor
def utility_processor():
    def inline_svg(filename):
        svg_path = os.path.join(app.static_folder, "svg", filename)
        try:
            with open(svg_path, "r", encoding="utf-8") as f:
                return Markup(
                    f.read()
                )  # Markup prevents Jinja from escaping the content
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


@app.post("/start")
@ensure_session
def start():
    """Start the session tasks, aswell as clone the repo from given link"""
    uid = session.get("_id")
    data = request.json
    git_link = data.get("git_link")
    if not validators.url(git_link):
        return jsonify({"error": "Not a valid url"})
    init_progress(uid)
    save_progress(uid,{"git_link":git_link,"task_state":"pending"})
    result = start_clone_git.apply_async(args=[session.get("_id")])
    save_progress(uid, {"current_task_id": result.id})
    return jsonify({"success": "Task created"})

@app.post("/process")
@ensure_session
def process():
    """Given a list of files/paths from the user repo, start the processing (parsing) and prompting process"""
    uid = session.get("_id")
    # check if that user even is at the reviewing step
    progress = get_progress(uid)
    if progress.get("state")!="select":
        return jsonify({"error": f"Not correct processing order ({progress.get("state")})"})
    data = request.json
    files = data.get("files")
    # check if at least some of the selected files are valid.
    if not all(file.endswith(".py") for file in files) or len(files)==0:
        return jsonify({"error": "All files must have a .py extension"})
    print("files:",files)
    save_progress(uid,{"files_to_process":files,"task_state":"pending"})
    result = process_files.apply_async(args=[session.get("_id")])
    save_progress(uid, {"current_task_id": result.id})
    return jsonify({"success": "Task created"})

@app.get("/docs")
@ensure_session
def docs():
    """Generate the documentation for the repo, using the updated docstrings"""
    uid = session.get("_id")
    progress = get_progress(uid)
    if progress.get("state") != "review":
        return jsonify({"error": f"Not correct processing order ({progress.get('state')})"})
    
    result = generate_docs.apply_async(args=[session.get("_id")])
    save_progress(uid, {"current_task_id": result.id})


# route to check if a task is done
@app.get("/progress")
@ensure_session
def progress() -> dict[str, object]:
    uid = session.get("_id")
    data = get_progress(uid)
    if not data:
        return jsonify({"error": "No Running Tasks!"})
    # TODO: DONT just send out data, for now its okay, but change later pls
    return jsonify(data)

@app.post("/changes")
@ensure_session
def changes()->dict[str,object]:
    uid = session.get("_id")
    path:str = request.json.get("path")
    data = get_progress(uid)
    print(uid, path, data)
    if "result" in data:
        if not any(item.get("file") == path for item in data["result"]):
            return jsonify({"error": "No file with the specified path found"})
        file_data = next(item for item in data["result"] if item.get("file") == path)
        base_path = Path(f"/data/{uid}/")
        file_content = (base_path / path).read_text()
        return jsonify({
            "changes": file_data.get("prompt_result_file"),
            "original": file_content
        })
    return jsonify({"error": "No changes available"})

@app.post("/submit_review")
@ensure_session
def submit_review()->dict[str,object]:
    uid = session.get("_id")
    file_changes: dict[str,str] = request.json.get("file_changes")
    save_progress(uid, {"file_changes":file_changes,"task_state":"pending"})
    result = bundle_create_bundle.apply_async(args=[session.get("_id")])
    save_progress(uid, {"current_task_id": result.id})
    return jsonify({"success": "Task created"})


@app.get("/download_bundle")
@ensure_session
def download_bundle():
    uid = session.get("_id")
    bundle_path = Path(f"/data/{uid}/changes.bundle")
    if not bundle_path.exists():
        return jsonify({"error": "Bundle file not found"}), 404
    return send_file(str(bundle_path), as_attachment=True, download_name="changes.bundle")


@app.post("/start_sphinx")
@ensure_session
def start_sphinx()->dict[str,object]:
    uid = session.get("_id")
    selected_theme: dict[str,str] = request.json.get("selected_theme")
    save_progress(uid, {"state":"sphinx","selected_theme":selected_theme,"task_state":"pending"})
    result = generate_docs.apply_async(args=[session.get("_id")])
    save_progress(uid, {"current_task_id": result.id})
    return jsonify({"success": "Task created"})


@app.get("/download_sphinx")
@ensure_session
def download_sphinx():

    uid = session.get("_id")
    build_dir = Path(f"/data/docs/{uid}/build")
    if not build_dir.exists() or not build_dir.is_dir():
        return jsonify({"error": "Sphinx build directory not found"}), 404

    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp_zip:
        shutil.make_archive(tmp_zip.name[:-4], 'zip', root_dir=build_dir)
        zip_path = tmp_zip.name[:-4] + ".zip"

    return send_file(zip_path, as_attachment=True, download_name="sphinx_build.zip")