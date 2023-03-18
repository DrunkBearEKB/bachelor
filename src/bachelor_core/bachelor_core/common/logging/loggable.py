from typing import Optional

from bachelor_core.common.logging.struct_logger import StructLogger


class Loggable:
    def __init__(self, app_name: str, name: Optional[str] = None):
        if not name:
            name = app_name
        self.__logger = StructLogger(app_name, name)

    def log_debug(self, msg: str = "", **kwargs):
        return self.__logger.debug(msg, **kwargs)

    def log_info(self, msg: str = "", **kwargs):
        return self.__logger.info(msg, **kwargs)

    def log_warning(self, msg: str = "", **kwargs):
        return self.__logger.warning(msg, **kwargs)

    def log_error(self, msg: str = "", **kwargs):
        return self.__logger.error(msg, **kwargs)

    def log_critical(self, msg: str = "", **kwargs):
        return self.__logger.critical(msg, **kwargs)
