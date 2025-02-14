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

    def close(self):
        """
        Closes the database connection.
        """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            db_logger.info("Database connection closed.")


admin = DataBaseConnect("itstime_db", "admin", "pw_admin")
admin.connect()
admin.close()
