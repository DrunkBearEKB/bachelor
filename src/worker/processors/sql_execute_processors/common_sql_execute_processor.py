from typing import Set

import sqlalchemy

from bachelor_core.common.utils.dbhelper import DBHelper
from errors import InvalidTaskData
from processors.sql_execute_processors.base_db_clear_processor import BaseDBClearProcessor


class CommonSQLExecuteProcessor(BaseDBClearProcessor):
    def _execute_sql(self, dbhelper: DBHelper, task_payload):
        sql = task_payload.get("sql", None)
        if not sql:
            raise InvalidTaskData("`sql` is not defined!")
        dbhelper.session.execute(sqlalchemy.text(sql))

    def supported_topics(self) -> Set[str]:
        return {"sql_execute:common"}
