import copy
import json
import time
from typing import List

from bachelor_core.application.application import Application
from bachelor_core.application.plugins.dynamic_cfg import get_var_from_dynamic_cfg
from bachelor_core.common.utils.imports import resolve
from base_processor import BaseProcessor
from scheduler_wrapper.scheduler_wrapper import SchedulerWrapper
from scheduler_wrapper.task import Task


class Worker(Application):
    NAME = "worker"
    VERSION = "0.0.1"

    def __init__(self):
        Application.__init__(self)

        self.__scheduler = SchedulerWrapper(self)

    def run(self):
        super().run()

        processors = self.__load_processors()
        topics = set()
        for processor in processors:
            topics.update(processor.supported_topics())
        topics = list(topics)
        topics_wo_sleep = copy.copy(topics)
        topics_wo_sleep.remove("sleep")

        while True:
            task = self.__scheduler.get(topics=topics_wo_sleep)
            if not task:
                task = self.__scheduler.get(topics=topics)
            if task:
                is_task_processed = False
                for processor in processors:
                    if is_task_processed:
                        break
                    if task.topic in processor.supported_topics():
                        self.log_info(
                            f"found {processor.__class__.__name__} "
                            f"processor for task with task_id={task.id}"
                        )
                        res = processor.process_task(task)
                        if res:
                            self.__scheduler.done(task)
                        else:
                            self.__scheduler.failed(task)
                        is_task_processed = True
                        break

                if not is_task_processed:
                    self.log_warning(
                        f"no available processors for task with topic={task.topic}"
                    )
                    # self.__scheduler.enqueue(Task())
                    self.__scheduler.enqueue(task)
            else:
                self.log_warning(f"no available tasks")
                if get_var_from_dynamic_cfg(
                        "enqueue_sleep_task_on_no_available_tasks", False
                ):
                    self.__scheduler.enqueue(Task("sleep", json.dumps({"sleep_time": 5})))
                time.sleep(1)

    def __load_processors(self) -> List[BaseProcessor]:
        processors = []

        list_processors = self.config.get("processors", [])
        for processor_cls_path, processor_cfg in list_processors.items():
            cls = resolve(processor_cls_path)
            processors.append(cls(self, self.__scheduler, processor_cfg))

        return processors


if __name__ == "__main__":
    app = Worker()
    app.run()
