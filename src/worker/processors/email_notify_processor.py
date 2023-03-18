from typing import Set, Dict, Any

from base_processor import BaseProcessor
from bachelor_core.application.application import Application
from scheduler_wrapper.scheduler_wrapper import SchedulerWrapper
from scheduler_wrapper.task import Task


class EmailNotifyProcessor(BaseProcessor):
    def _process_task(self, task: Task):
        pass

    def supported_topics(self) -> Set[str]:
        return {"email_notify"}
