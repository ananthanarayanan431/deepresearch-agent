import logging.config

LOG_LEVEL: str = "INFO"
LOG_HANDLERS: list[str] = ["console", "file"]  # Can be ["console"], ["file"], or both

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(levelname)s] %(asctime)s | %(name)s | %(funcName)s:%(lineno)d | %(message)s",
        },
        "color": {
            "()": "colorlog.ColoredFormatter",
            "format": (
                "%(log_color)s[%(levelname)s] %(asctime)s | %(name)s | "
                "%(funcName)s:%(lineno)d | %(message)s"
            ),
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "color",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "app.log",
            "formatter": "color",
        },
    },
    "root": {
        "level": "NOTSET",
        "handlers": [],
    },
    "loggers": {
        "src": {
            "level": LOG_LEVEL,
            "handlers": LOG_HANDLERS,
            "propagate": False,
        }
    },
}


def setup_logging():
    """Setup logging configuration"""
    logging.config.dictConfig(LOGGING_CONFIG)
