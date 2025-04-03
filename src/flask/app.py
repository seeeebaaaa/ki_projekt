from flask import Flask, jsonify, request, render_template, session
from flask_session import Session
import requests
import celery_utils
import os
from redis import Redis
from flask_talisman import Talisman
from turbo_flask import Turbo
import uuid

app = Flask(__name__)
SESSION_TYPE = 'redis'
SESSION_REDIS = Redis(host=os.environ["REDIS_HOST"], port=os.environ["REDIS_PORT"])
app.config.from_object(__name__)
Session(app)
turbo = Turbo(app)
# Talisman(app) #breaks inline script, needs to be configured some how but idfk

@turbo.user_id
def get_user_id():
    return session["_id"]

# set up celery
app.config.from_mapping(
    CELERY=dict(
        broker_url=os.environ["CELERY_BROKER_URL"], # set via dockerfile
        result_backend=os.environ["CELERY_RESULT_BACKEND"], # set via dockerfile
        task_ignore_result=True,
    ),
)

celery_app = celery_utils.init_app(app)
@app.route('/', methods=['GET'])
def home():
    if "_id" not in session:
        # generate a new session id
        session["_id"] = uuid.uuid1()
    print(session)
    healthy = requests.get("http://ast:5000/healthy")
    return render_template("index.html", healthy=healthy.text)


@app.route('/getLower', methods=['POST'])
def get_lower_data():
    data = request.json
    code = data['code']
    response = requests.post("http://ast:5000/toLower", json={"code": code})
    return jsonify(response.json())


@app.route('/process', methods=['POST'])
def py_file():
    return jsonify({"message": "File parsed successfully."})