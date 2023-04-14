import os
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/", methods=["POST"])
def hello_world():
    target = os.environ .get("TARGET", "World")
    resp = {
        "host": request.headers["Host"],
        "user-agent": request.headers["User-Agent"],
        "timestamp": datetime.now().isoformat(),
        "data": "Hello {}!\n".format(target),
        "form": request.form,
        "json": request.get_json()
    }
    return jsonify(resp)

@app.route("/health-check", methods=["GET"])
def healthcheck():
    return "success"