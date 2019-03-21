import os
from flask import Flask, request, abort
from flask_pymongo import PyMongo


mongo_uri = (
    f"mongodb://{os.environ['MONGO_USER']}:{os.environ['MONGO_PASS']}@"
    f"{os.environ['MONGO_HOST']}:{os.environ['MONGO_PORT']}/{os.environ['MONGO_DB']}"
)

application = Flask(__name__)
application.config["MONGO_URI"] = mongo_uri
mongo = PyMongo(application)


@application.route("/auth", methods=["POST"])
def auth():
    username = None
    try:
        token = request.form["token"]
        user_rec = mongo.db.users.find_one({"token": token})
    except Exception as e:
        abort(500, e)
    else:
        if user_rec:
            username = user_rec["username"]
    return username if username else abort(403)


@application.route("/healthz")
def healthz():
    try:
        mongo.db.users.find_one()
    except Exception as e:
        abort(500, e)
    else:
        return "OK"


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5001)
