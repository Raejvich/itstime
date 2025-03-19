import psycopg2
import logging
from psycopg2.extras import DictCursor
from typing import List, Tuple, Any, Optional
import datetime
import json


class DataBaseConnect:

    def __init__(
        self,
        dbname: str,
        user: str,
        password: str,
        host: str = "localhost",
        port: str = "5432",
    ):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            )
            # Enables dictionary-like query results
            self.cursor = self.conn.cursor(cursor_factory=DictCursor)
            logging.info("Connecter to database successfully")
        except psycopg2.Error as e:
            logging.error(f"Error connecting to database: {e}")

    def execute_query(
        self, query: str, params: Optional[Tuple[Any, ...]] = None
    ) -> List[Tuple]:
        """
        Executes a SQL query and fetches results if applicable.

        :param query: SQL query string.
        :param params: Optional tuple of parameters.
        :return: List of tuples containing query results.
        """
        try:
            self.cursor.execute(query, params or ())
            if (
                query.strip().lower().startswith("select")
                or "returning" in query.lower()
            ):
                results = self.cursor.fetchall()
                logging.info(f"Executed SELECT query: {query}")
                return results
            logging.info(f"Executed query: {query} with params {params}")
        except psycopg2.Error as e:
            logging.error(
                f"Error executing query: {e} | Query: {query} | Params: {params}"
            )
            self.conn.rollback()
        return []

    def insert_event(self, event_name: str, event_date: datetime, event_location: str):
        """
        Inserts a new event into the database.
        """
        query = """
        INSERT INTO events (name, event_date, location)
        VALUES (%s, %s, %s)
        RETURNING id;
        """
        result = self.execute_query(query, (event_name, event_date, event_location))
        logging.info(f"Inserted event: {event_name} on {event_date}")
        return result[0][0]

    def insert_fight(self, event_id, fighter_1, fighter_2, fight_order):
        """
        Inserts fight data into database
        """
        query = """
        INSERT INTO fights (event_id, fighter_1, fighter_2, fight_order)
        VALUES (%s, %s, %s, %s)
        """
        self.execute_query(query, (event_id, fighter_1, fighter_2, fight_order))
        logging.info(f"Inserted fight: {fight_order} in event {event_id}")

    def fetch_events(self) -> List[Tuple]:
        """
        Retrieves all events from the database.
        """
        query = "SELECT * FROM events;"
        results = self.execute_query(query)
        logging.info(f"Fetched {len(results)} events from database.")
        return results

    def fetch_fights(self, event_id):
        """
        Retrieves all fights for a specific event from the database.
        """
        query = "SELECT * FROM fights WHERE event_id = %s;"
        results = self.execute_query(query, (event_id,))  # Pass event_id as a parameter
        logging.info(
            f"Fetched {len(results)} fights from database for event_id: {event_id}"
        )
        return results

    def fetch_event_ids(self):
        """
        Retrieves all events from the database.
        """
        query = "SELECT id FROM events;"
        results = self.execute_query(query)
        logging.info(f"Fetched {len(results)} event id's from database.")
        return results

    def delete_events(self):
        query = "DELETE FROM events;"
        self.execute_query(query)
        logging.info(f"Deleted events from database.")

    def close(self):
        """
        Closes the database connection.
        """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            logging.info("Database connection closed.")


if __name__ == "__main__":

    with open(r"src\database\db_credentials.json", "r") as file:
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
