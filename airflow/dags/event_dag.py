import sys
import os

# Add the /opt/src folder to the Python path so the scraper module can be found
sys.path.append("/opt/src")

from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from scrape.scrape_tapology import WebScraper
from database.database import DataBaseConnect
import json

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 3, 9),
    "email": ["gustav.6.johansson@hotmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}


def scrape_tapology():
    # Create web scraper object
    scraper = WebScraper()
    # get raw event data
    scraper.get_event_data()
    # get structured data
    scraper.structure_data()

    with open("../src/database/db_credentials.json", "r") as file:
        db_credentials = json.load(file)

    admin = DataBaseConnect(
        db_credentials["database"],
        db_credentials["username"],
        db_credentials["password"],
        "host.docker.internal",
    )
    # connect to DB
    admin.connect()
    # delete current events
    admin.delete_events()
    # iterate through every event an insert into DB
    for event in scraper.structured_event_data:
        id = admin.insert_event(
            event_name=event.event_name,
            event_date=event.event_date,
            event_location=event.event_location,
        )
        for order, fight in enumerate(event.event_fights):
            admin.insert_fight(
                event_id=id, fighter_1=fight[0], fighter_2=fight[1], fight_order=order
            )
    # commit deletion and insert at the same time
    admin.conn.commit()
    admin.close()


with DAG(
    "test_dag", default_args=default_args, schedule="@weekly", catchup=False
) as dag:

    scrape_tapology = PythonOperator(
        task_id="run_scraper",
        python_callable=scrape_tapology,
    )
