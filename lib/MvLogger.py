import logging
import os
import sys

from lib import Utilities


def get_current_directory():
    if getattr(sys, 'frozen', False):  # Check if running as an executable
        return os.path.dirname(sys.executable)
    else:  # Running as a script
        return os.path.dirname(os.path.abspath(__file__))


def get_logger(logger_name) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logger_level = Utilities.get_stored_ini_value("Loggers", logger_name, "Settings")
    if logger_level == "DEBUG":
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(get_current_directory() + "\\MvRunLog.txt")
    if logger_level == "DEBUG":
        file_handler.setLevel(logging.DEBUG)
    else:
        file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
