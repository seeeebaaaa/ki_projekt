from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/toLower', methods=['POST'])
def toLower():
    """just a test route to check if the flask app is working"""
    data = request.json
    code = data['code']    
    return jsonify(code.lower())


@app.route('/healthy', methods=['GET'])
def healthy():
    """Route that povides an endpoint for the docker healthcheck."""
    return "yay"

@app.route('/py/file', methods=['POST'])
def py_file():
    return "nothing"
