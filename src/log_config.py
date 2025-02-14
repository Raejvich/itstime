import os
import logging
from logging.handlers import RotatingFileHandler

# Create logs directory if it doesn't exist
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


# Function to create a logger with a rotating file handler
def setup_logger(name: str, log_file: str, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create a rotating file handler
    log_path = os.path.join(LOG_DIR, log_file)
    file_handler = RotatingFileHandler(
        log_path, maxBytes=5 * 1024 * 1024, backupCount=5
    )
    file_handler.setLevel(level)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Set up loggers for different parts of the application
pipeline_logger = setup_logger("PipelineLogger", "pipeline.log")
api_logger = setup_logger("APILogger", "api.log")
db_logger = setup_logger("DatabaseLogger", "database.log")
frontend_logger = setup_logger("FrontendLogger", "frontend.log")
