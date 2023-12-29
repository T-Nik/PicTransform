# logger_config.py
import logging
LOGGING_FILENAME = 'logfile.log'

def setup_logging():
    logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)
