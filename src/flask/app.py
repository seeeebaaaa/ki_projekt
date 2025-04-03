from flask import Flask, jsonify, request, render_template
import requests


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    healthy = requests.get("http://ast:5000/healthy")
    return render_template("index.html", healthy=healthy.text)


@app.route('/getLower', methods=['POST'])
def get_lower_data():
    data = request.json
    code = data['code']
    response = requests.post("http://ast:5000/toLower", json={"code": code})
    return jsonify(response.json())