import os
import logging
from logging.config import dictConfig
from typing import Dict, Optional


SIMPOLL_DEFAULT_HELLO_WORLD = os.environ.get(
    "SIMPOLL_DEFAULT_HELLO_WORLD",
    default="world",
)

SIMPOLL_LOG_LEVEL = os.getenv("SIMPOLL_LOG_LEVEL", "INFO")

SIMPOLL_JWT_ENCRYPTION_ALGORITHM = os.environ.get(
    "SIMPOLL_JWT_ENCRYPTION_ALGORITHM",
    default="HS256"
)


SIMPOLL_FLASK_HOST = os.environ.get(
    "SIMPOLL_FLASK_HOST",
    default="127.0.0.1",
)

SIMPOLL_FLASK_PORT = os.environ.get(
    "SIMPOLL_FLASK_PORT",
    default="8080"
)


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


logger = get_logger(name=__name__)


def _get_default_jwt_secret_key() -> str:
    logger.warning("Using the default JWT Secret Key.")
    return "default"


def get_jwt_secret_key() -> str:
    return os.environ.get("SIMPOLL_JWT_SECRET_KEY") or _get_default_jwt_secret_key()
