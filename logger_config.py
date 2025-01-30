# logger_config.py
import logging
from datetime import datetime


# Configure the logger
logger = logging.getLogger("azure_file_processor")  # Unique logger name
logger.setLevel(logging.INFO)  # Set the base logging level

# Check if handlers are already added
if not logger.handlers:
    # Create a formatter with the desired format
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(filename)s : %(funcName)s : %(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Create a console handler and set the formatter
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File handler
    # file_handler = logging.FileHandler("app.log")
    # file_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(console_handler)
    # logger.addHandler(file_handler)
