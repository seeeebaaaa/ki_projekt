from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/toLower', methods=['POST'])
def toLower():
    data = request.json
    code = data['code']    
    return jsonify(code.lower())


@app.route('/healthy', methods=['GET'])
def healthy():
    return "yay"
