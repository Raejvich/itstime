from flask import Flask, render_template
import json
from src.database.database import DataBaseConnect
import datetime

app = Flask(__name__)


@app.route("/")
def home():

    with open("src/database/db_credentials.json", "r") as file:
        db_credentials = json.load(file)

    admin = DataBaseConnect(
        db_credentials["database"],
        db_credentials["username"],
        db_credentials["password"],
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
    app.run(debug=True, use_reloader=False)
