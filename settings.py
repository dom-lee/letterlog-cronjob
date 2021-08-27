import os
import logging

DB_HOST       = os.environ.get('DB_HOST')
DB_PORT       = os.environ.get('DB_PORT')
DB_USER       = os.environ.get('DB_USER')
DB_PASSWORD   = os.environ.get('DB_PASSWORD')
DB_ENGINE_URL = f'mysql+mysqldb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/letterlog'

GMAIL_USER = os.environ.get('GMAIL_USER')
GMAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD')


# create logger
def get_logger(name=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter("%(asctime)s; %(message)s")

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    return logger