import psycopg2
import logging
from src.log_config import db_logger

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
            db_logger.info("Connecter to database successfully")
        except psycopg2.Error as e:
            db_logger.error(f"Error connecting to database: {e}")


admin = DataBaseConnect("itstime_db", "admin", "pw_admin")
admin.connect()
