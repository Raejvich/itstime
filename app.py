from flask import Flask, render_template
import json
from src.database.database import DataBaseConnect
import datetime

app = Flask(__name__)

try:
    with open("src/database/db_credentials.json", "r") as file:
        db_credentials = json.load(file)

    admin = DataBaseConnect(
        db_credentials["database"],
        db_credentials["username"],
        db_credentials["password"],
    )
    admin.connect()
    events = admin.fetch_events()
    admin.close()
    print(f"Fetched events: {events}")  # Debugging output
except Exception as e:
    print(f"Database connection error: {e}")
    events = []  # Fallback to an empty list so Flask still runs


@app.route("/")
def home():
    return render_template("index.html", events=events)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
