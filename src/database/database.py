import psycopg2
import logging
from src.log_config import db_logger
from psycopg2 import sql
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
            db_logger.info("Connecter to database successfully")
        except psycopg2.Error as e:
            db_logger.error(f"Error connecting to database: {e}")

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
                db_logger.info(f"Executed SELECT query: {query}")
                return results
            db_logger.info(f"Executed query: {query} with params {params}")
        except psycopg2.Error as e:
            db_logger.error(
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
        db_logger.info(f"Inserted event: {event_name} on {event_date}")
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
        db_logger.info(f"Inserted fight: {fight_order} in event {event_id}")

    def fetch_events(self) -> List[Tuple]:
        """
        Retrieves all events from the database.
        """
        query = "SELECT * FROM events;"
        results = self.execute_query(query)
        db_logger.info(f"Fetched {len(results)} events from database.")
        return results

    def delete_events(self):
        query = "DELETE FROM events;"
        self.execute_query(query)
        db_logger.info(f"Deleted events from database.")

    def close(self):
        """
        Closes the database connection.
        """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            db_logger.info("Database connection closed.")


if __name__ == "__main__":

    with open(r"src\database\db_credentials.json", "r") as file:
        db_credentials = json.load(file)

    admin = DataBaseConnect(
        db_credentials["database"],
        db_credentials["username"],
        db_credentials["password"],
    )
    admin.connect()
    print(admin.fetch_events())
