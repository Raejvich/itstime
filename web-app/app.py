import sys
import os

sys.path.append("/opt/src")
from flask import Flask, render_template
import json
from database.database import DataBaseConnect
import datetime


app = Flask(__name__)


@app.route("/")
def home():

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    print(DB_USER)
    print(DB_PASSWORD)
    print(DB_NAME)
    print(DB_HOST)
    admin = DataBaseConnect(
        DB_NAME,
        DB_USER,
        DB_PASSWORD,
        DB_HOST,
    )
    admin.connect()
    events = admin.fetch_events()
    event_ids = admin.fetch_event_ids()
    fight_dict = dict()
    for event_id in event_ids:
        fights = admin.fetch_fights(event_id[0])
        fight_list = [fight[2:4] for fight in fights]
        fight_dict[event_id[0]] = fight_list

    admin.close()

    return render_template("index.html", events=events, fight_dict=fight_dict)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, use_reloader=False)
