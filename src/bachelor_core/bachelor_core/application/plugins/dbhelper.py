from typing import Dict, Any

from bachelor_core.application.application import Application
from bachelor_core.application.base_plugin import BasePlugin
from bachelor_core.common.utils.dbhelper import DBHelper, Session


class DBHelperPlugin(BasePlugin):
    """
    Плагин для использования БД
    """

    NAME = "dbhelper"
    PLUGIN_INSTALL = [
        "session",
        "commit",
    ]

    def __init__(self, app: Application, config: Dict[str, Any]):
        super().__init__(app, config)

        db_id = config.get("db_id", None)
        if not db_id:
            raise Exception()  # TODO: add custom exception with message
        self.__db_helper = DBHelper(db_id)

    @property
    def session(self) -> Session:
        return self.__db_helper.session

    def commit(self):
        self.log_info("committing: started")
        try:
            res = self.__db_helper.commit()
            self.log_info("committing: finished")
            return res
        except Exception as e:
            self.log_error("committing: failed", error=e)
            raise
