import logging
import logging.config
import os
from pathlib import Path

LOG_DIR = Path(os.getenv("LOG_DIR", "logs"))
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
TELEBOT_LEVEL = os.getenv("TELEBOT_LEVEL", "WARNING").upper()

class ContextAdapter(logging.LoggerAdapter):
    """Лог-адаптер, добавляет контекст tg_id, chat_id, username и др."""
    def process(self, msg, kwargs):
        ctx = " ".join(f"{k}={v}" for k, v in self.extra.items() if v is not None)
        if ctx:
            return f"{ctx} | {msg}", kwargs
        return msg, kwargs

def setup_logging():
    """
        Вызывать один раз при старте приложения (в __main__).
    """
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "rich": {
                "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
            },
            "verbose": {
                "format": (
                    "%(asctime)s %(levelname)s %(name)s "
                    "[pid=%(process)d tid=%(threadName)s] "
                    "%(module)s:%(lineno)d | %(message)s"
                )
            },
            # Для JSON можно подключить сторонний форматтер (loguru/structlog), но держим stdlib.
        },
        "handlers": {
            # Консоль — удобно под systemd/docker
            "console": {
                "class": "logging.StreamHandler",
                "level": LOG_LEVEL,
                "formatter": "rich",
            },
            # Ротация по времени — дневные файлы, хранить 14 штук
            "file_timed": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "level": LOG_LEVEL,
                "formatter": "verbose",
                "filename": str(LOG_DIR / "bot.log"),
                "when": "midnight",
                "backupCount": 14,
                "encoding": "utf-8",
                "utc": False,  # вам удобнее локальное время Europe/Podgorica
            },
            # Альтернатива: ротация по размеру (раскомментируйте при желании)
            # "file_size": {
            #     "class": "logging.handlers.RotatingFileHandler",
            #     "level": LOG_LEVEL,
            #     "formatter": "verbose",
            #     "filename": str(LOG_DIR / "bot.log"),
            #     "maxBytes": 10 * 1024 * 1024,  # 10 MB
            #     "backupCount": 5,
            #     "encoding": "utf-8",
            # },
        },
        "loggers": {
            # Ваше приложение
            "rotation_bot": {"level": LOG_LEVEL, "handlers": ["console", "file_timed"], "propagate": False},
            "db": {"level": LOG_LEVEL, "handlers": ["console", "file_timed"], "propagate": False},
            "voting": {"level": LOG_LEVEL, "handlers": ["console", "file_timed"], "propagate": False},

            # Третьи стороны — притушим
            "telebot": {"level": TELEBOT_LEVEL, "handlers": ["console", "file_timed"], "propagate": False},
            "urllib3": {"level": "WARNING", "handlers": ["console", "file_timed"], "propagate": False},
        },
        "root": {
            "level": LOG_LEVEL,
            "handlers": ["console", "file_timed"]
        },
    }
    logging.config.dictConfig(config)

    # Логировать предупреждения из модуля warnings
    logging.captureWarnings(True)

    # Перехват неотловленных исключений
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            return
        logging.getLogger("rotation_bot").exception("UNCAUGHT: %s", exc_value,
                                                    exc_info=(exc_type, exc_value, exc_traceback))

    import sys
    sys.excepthook = handle_exception