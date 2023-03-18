import abc
from typing import Set, Dict, Any

import sqlalchemy

from bachelor_core.common.utils.dbhelper import DBHelper
from processors.sql_execute_processors.base_db_clear_processor import BaseDBClearProcessor


SQL = """
DELETE
FROM scheduler.tasks
WHERE LENGTH(finish_dt) != 0;
"""


class SchedulerDBClearProcessor(BaseDBClearProcessor, abc.ABC):
    def _clear(self, dbhelper: DBHelper, task_payload: Dict[str, Any]):
        dbhelper.session.execute(sqlalchemy.text(SQL))

    def supported_topics(self) -> Set[str]:
        raise {"sql_execute:clear:scheduler_db"}
