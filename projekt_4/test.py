from .app import app, ensure_session
from flask import jsonify, request, session
import requests
from celery.result import AsyncResult

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
