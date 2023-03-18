import time
from typing import Set

from bachelor_core.application.plugins.dynamic_cfg import get_var_from_dynamic_cfg
from base_processor import BaseProcessor
from scheduler_wrapper.task import Task


class SleepProcessor(BaseProcessor):
    def _process_task(self, task: Task):
        sleep_time = task.payload.get("sleep_time", 5)
        time.sleep(sleep_time)
        if get_var_from_dynamic_cfg("enqueue_sleep_task_on_finish", False):
            self.scheduler.enqueue(task)

    def supported_topics(self) -> Set[str]:
        return {"sleep"}
