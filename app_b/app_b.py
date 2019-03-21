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
    try:
        token = request.form["token"]
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute("SELECT username from users where token = (?) LIMIT 1", (token,))
        username = cur.fetchone()[0]
        con.close()
        return username
    except:
        return "fail"


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5001)
