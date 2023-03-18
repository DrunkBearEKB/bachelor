import logging
from typing import Dict


LOGGER_FMT = (
    "%(asctime)s P%(process)d T%(thread)d %(levelname)s %(name)s: %(message)s"
)


class StructLogger:
    REMOVABLE_LOGGERS = ["werkzeug"]

    def __init__(self, app_name: str, name: str):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        log_filename = f"./logs/{app_name}.log"
        if log_filename:
            file_handler = logging.FileHandler(log_filename)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(logging.Formatter(LOGGER_FMT))
            logger.addHandler(file_handler)
        logger.propagate = False

        self.__logger = logger

    def debug(self, msg: str, **kwargs: Dict[str, object]):
        return self.__log(logging.DEBUG, msg, **kwargs)

    def info(self, msg: str, **kwargs: Dict[str, object]):
        return self.__log(logging.INFO, msg, **kwargs)

    def warning(self, msg: str, **kwargs: Dict[str, object]):
        return self.__log(logging.WARNING, msg, **kwargs)

    def error(self, msg: str, **kwargs: Dict[str, object]):
        return self.__log(logging.ERROR, msg, **kwargs)

    def critical(self, msg: str, **kwargs: Dict[str, object]):
        return self.__log(logging.CRITICAL, msg, **kwargs)

    def __log(self, level: int, msg, **kwargs):
        msg_formatted = self.__format_log_data(msg, **kwargs)
        self.__logger.log(level, msg_formatted)

    @staticmethod
    def __format_log_data(msg: str, **kwargs: Dict[str, object]) -> str:
        result = msg.strip() + "  " + (
            ", ".join([f"{k}: {v}" for k, v in kwargs.items()]) if kwargs else ""
        )
        return result.strip()
