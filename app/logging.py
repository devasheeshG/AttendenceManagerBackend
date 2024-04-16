# Path: app/logging.py
# Description: Logging configuration for the application.

import logging
# from fastapi.logger import logger

# TODO: Fix the logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

# logger = logging.getLogger(__name__)
# logger = logging.getLogger("fastapi")
logger = logging.getLogger("uvicorn")

if __name__ == "__main__":
    # Log messages
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")