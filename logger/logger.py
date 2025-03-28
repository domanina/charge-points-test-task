import logging.config
import sys
import logging.config


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "default_formatter": {
            "format": f"\n%(levelname)-8s %(asctime)s [%(filename)s:%(lineno)d] %(message)s"
        },
    },

    "handlers": {
        "stream_handler": {
            "class": "logging.StreamHandler",
            "formatter": "default_formatter",
            "stream": sys.stdout
        },
    },

    "loggers": {
        "main_logger": {
            "handlers": ["stream_handler"],
            "level": "DEBUG",
            "propagate": True
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("main_logger")


def get_logger(name: str = None):
    """
           Get a logger.

           :param name: name of a logger, default None.
           :return: A logger.
    """
    logger = logging.getLogger(name if name else "main_logger")
    if not logger.handlers:
        parent_logger = logging.getLogger("main_logger")
        for handler in parent_logger.handlers:
            logger.addHandler(handler)
        logger.setLevel(parent_logger.level)
    return logger
