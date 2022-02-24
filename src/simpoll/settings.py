import os
import logging
from logging.config import dictConfig
from typing import Dict, Optional


SIMPOLL_DEFAULT_HELLO_WORLD = os.environ.get(
    "SIMPOLL_DEFAULT_HELLO_WORLD",
    default="world",
)

SIMPOLL_LOG_LEVEL = os.getenv("SIMPOLL_LOG_LEVEL", "INFO")

logger_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            "level": SIMPOLL_LOG_LEVEL,
            "propagate": True
        }
    }
}


def get_logger(name: str, logger_config_dictionary: Optional[Dict] = None):
    config = logger_config_dictionary or logger_config
    dictConfig(config)
    return logging.getLogger(name)
