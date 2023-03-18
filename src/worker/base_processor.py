import abc
from typing import Set, Dict, Any

from bachelor_core.application.application import Application
from scheduler_wrapper.scheduler_wrapper import SchedulerWrapper
from scheduler_wrapper.task import Task


class BaseProcessor(abc.ABC):
    def __init__(
            self, app: Application, scheduler: SchedulerWrapper, config: Dict[str, Any]
    ):
        self.__app = app
        self.__scheduler = scheduler
        self.__config = config

    def process_task(self, task: Task):
        try:
            self.__app.log_info("task started", task_id=task.id, topic=task.topic)
            self._process_task(task)
            self.__app.log_info("task finished", task_id=task.id)
            return True
        except KeyboardInterrupt:
            raise
        except Exception as e:
            self.__app.log_info("task failed", task_id=task.id, exception=str(e))
        return False

    @abc.abstractmethod
    def _process_task(self, task: Task):
        raise NotImplementedError()

    @abc.abstractmethod
    def supported_topics(self) -> Set[str]:
        raise NotImplementedError()

    @property
    def app(self) -> Application:
        return self.__app

    @property
    def scheduler(self) -> SchedulerWrapper:
        return self.__scheduler

    @property
    def config(self) -> Dict[str, Any]:
        return self.__config
