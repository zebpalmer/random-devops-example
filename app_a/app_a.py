import os
from flask import Flask, request, abort
import requests

application = Flask(__name__)


@application.route("/hello")
def hello():
    return "Hello there"


@application.route("/jobs", methods=["POST"])
def jobs():
    token = request.headers["Authorization"]
    data = {"token": token}
    result = requests.post(f"http://{os.environ['AUTH_SVC']}/auth", data=data, timeout=5)
    if result.content == b"density":
        return "Jobs:\nTitle: Devops\nDescription: Awesome\n"
    else:
        return "fail"


@application.route("/healthz")
def healthz():
    try:
        res = requests.get(f"http://{os.environ['AUTH_SVC']}/healthz", timeout=5)
        if res.status_code != 200:
            abort(500, f"auth svc health status: {res.status_code}")
    except Exception as e:
        abort(500, f"Failed contacting auth service health endpoint: {e}")
    else:
        return "OK"


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000)
