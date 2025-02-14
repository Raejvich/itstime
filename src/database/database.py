import psycopg2
import logging
from src.log_config import db_logger
from psycopg2 import sql
from psycopg2.extras import DictCursor
from typing import List, Tuple, Any, Optional


# Configure logging
logging.basicConfig(
    filename=r"C:\Users\Gustav\repos\itstime\src\logs\database.log",  # Log file name
    level=logging.INFO,  # Log level (INFO, WARNING, ERROR)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    datefmt="%Y-%m-%d %H:%M:%S",  # Date format
)


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
            if query.strip().lower().startswith("select"):
                results = self.cursor.fetchall()
                db_logger.info(f"Executed SELECT query: {query}")
                # Return results if it's a SELECT query
                return results
            # Commit transaction for INSERT, UPDATE, DELETE
            self.conn.commit()
            db_logger.info(f"Executed query: {query} with params {params}")
        except psycopg2.Error as e:
            db_logger.error(
                f"Error executing query: {e} | Query: {query} | Params: {params}"
            )
            self.conn.rollback()
        return []

    def insert_event(self, event_name: str, event_date: str, event_time: str):
        """
        Inserts a new event into the database.
        """
        query = """
        INSERT INTO events (event_name, event_date, event_time)
        VALUES (%s, %s, %s);
        """
        self.execute_query(query, (event_name, event_date, event_time))
        db_logger.info(f"Inserted event: {event_name} on {event_date}")

    def fetch_events(self) -> List[Tuple]:
        """
        Retrieves all events from the database.
        """
        query = "SELECT * FROM events;"
        results = self.execute_query(query)
        db_logger.info(f"Fetched {len(results)} events from database.")
        return results

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
    admin = DataBaseConnect("itstime_db", "admin", "pw_admin")
    admin.connect()
    admin.insert_event("test_name", "2022-01-01", "18:00:00")
    admin.fetch_events()
    admin.close()
