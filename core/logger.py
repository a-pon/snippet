import logging.handlers
import multiprocessing

LOG_FILE = 'logs/my_app.log'

log_queue = multiprocessing.Queue()

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(levelname)s: %(message)s",
        },
        "detailed": {
            "format": "[%(levelname)s|%(module)s|L%(lineno)d] %(asctime)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "WARNING",
            "formatter": "simple",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": LOG_FILE,
            "maxBytes": 10000,
            "backupCount": 3,
        },
        "queue": {
            "class": "logging.handlers.QueueHandler",
            "queue": log_queue,
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["queue"],
    },
}

listener = logging.handlers.QueueListener(
    log_queue,
    logging.StreamHandler(),
    logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=10000, backupCount=3))
