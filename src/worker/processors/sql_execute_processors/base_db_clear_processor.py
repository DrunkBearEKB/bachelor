import abc
from typing import Set, Dict, Any

from bachelor_core.common.utils.dbhelper import DBHelper
from processors.base_sql_execute_processor import BaseSQLExecuteProcessor


class BaseDBClearProcessor(BaseSQLExecuteProcessor, abc.ABC):
    def _execute_sql(self, dbhelper: DBHelper, task_payload: Dict[str, Any]):
        self._clear(dbhelper, task_payload)

    @abc.abstractmethod
    def _clear(self, dbhelper: DBHelper, task_payload: Dict[str, Any]):
        raise NotImplementedError()

    @abc.abstractmethod
    def supported_topics(self) -> Set[str]:
        raise NotImplementedError()
