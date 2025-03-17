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
    "retries": 0,
    "retry_delay": timedelta(minutes=2),
}


def scrape_tapology():
    # Create web scraper object
    scraper = WebScraper()
    # get raw event data
    scraper.get_event_data()
    # get structured data
    scraper.structure_data()

    event_list = scraper.structured_event_data

    return event_list


def load_db():
    pass


def connect_db(task_instance):
    event_list = task_instance.xcom_pull(task_ids="run_scraper")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    admin = DataBaseConnect(
        DB_NAME,
        DB_USER,
        DB_PASSWORD,
        DB_HOST,
    )
    # connect to DB
    admin.connect()
    # delete current events
    admin.delete_events()
    # iterate through every event an insert into DB
    for event in event_list:
        id = admin.insert_event(
            event_name=event["event_name"],
            event_date=event["event_date"],
            event_location=event["event_location"],
        )
        for order, fight in enumerate(event["event_fights"]):
            admin.insert_fight(
                event_id=id, fighter_1=fight[0], fighter_2=fight[1], fight_order=order
            )
    # commit deletion and insert at the same time
    admin.conn.commit()
    admin.close()


with DAG(
    "event_dag", default_args=default_args, schedule="@weekly", catchup=False
) as dag:

    scrape = PythonOperator(
        task_id="run_scraper",
        python_callable=scrape_tapology,
    )

    load_to_db = PythonOperator(
        task_id="load_db",
        python_callable=connect_db,
    )

    scrape >> load_to_db
