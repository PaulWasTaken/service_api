import logging

from config.logger_config import LOGS_PATH, LOG_LEVEL

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler(LOGS_PATH)
file_handler.setLevel(LOG_LEVEL)
file_handler.setFormatter(formatter)


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    logger.addHandler(file_handler)
    return logger
