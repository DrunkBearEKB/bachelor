import abc
from typing import Set

from bachelor_core.common.utils.dbhelper import DBHelper
from errors import InvalidTaskData
from scheduler_wrapper.task import Task
from base_processor import BaseProcessor


class BaseSQLExecuteProcessor(BaseProcessor, abc.ABC):
    def _process_task(self, task: Task):
        db_id = task.payload.get("db_id", None)
        if not db_id:
            raise InvalidTaskData("`db_id` is not defined!")

        dbhelper = DBHelper(db_id)
        self._execute_sql(dbhelper, task.payload)

    @abc.abstractmethod
    def _execute_sql(self, dbhelper: DBHelper, task_payload):
        raise NotImplementedError()

    @abc.abstractmethod
    def supported_topics(self) -> Set[str]:
        raise NotImplementedError()
