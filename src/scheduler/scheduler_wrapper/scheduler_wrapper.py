from typing import List, Optional

from bachelor_core.application.application import Application
from bachelor_core.application.wrapper.base_rest_wrapper import BaseRESTWrapper
from bachelor_core.common.http.requests import http_get, http_post

from scheduler_wrapper.task import Task


class SchedulerWrapper(BaseRESTWrapper):
    def __init__(self, app: Application):
        BaseRESTWrapper.__init__(self, app, "scheduler", "scheduler")

    def enqueue(self, task: Task):
        self.log_info("enqueueing task: started", task_id=task.id)
        try:
            response = http_post(
                url=f"{self.url}/task/enqueue",
                json={"task": task.get_json_to_export()},
            )
            if response.status_code == 200:
                self.log_info("enqueueing task: finished", task_id=task.id)
                return
            self.log_info("enqueueing task: failed", task_id=task.id)
        except Exception as e:
            self.log_error("enqueueing task: failed", task_id=task.id, error=e)
            raise e

    def get(self, topics: List[str]) -> Optional[Task]:
        self.log_info("getting task: started", topics=topics)
        try:
            response = http_get(
                url=f"{self.url}/task/get",
                json={"topics": topics},
            )
            response_json = response.json()
            task_data = response_json.get("task", {})
            if task_data:
                task = Task.deserialize(task_data)
                self.log_info("getting task: finished", task_id=task.id)
                return task
            self.log_warning("getting task: finished - no available tasks")
            return
        except Exception as e:
            self.log_error("getting task: failed", topics=topics, error=e)
            raise e

    def done(self, task: Task):
        self.log_info("marking task as done: started", task_id=task.id)
        try:
            http_post(
                url=f"{self.url}/task/done",
                json={"task_id": task.id},
            )
            self.log_info("marking task as done: finished", task_id=task.id)
        except Exception as e:
            self.log_error("marking task as done: failed", task_id=task.id, error=e)
            raise e

    def failed(self, task: Task):
        self.log_info("marking task as failed: started", task_id=task.id)
        try:
            http_post(
                url=f"{self.url}/task/failed",
                json={"task_id": task.id},
            )
            self.log_info("marking task as failed: finished", task_id=task.id)
        except Exception as e:
            self.log_error("marking task as failed: failed", task_id=task.id, error=e)
            raise e

    def cancel(self, task: Task):
        self.log_info("cancelling task: started", task_id=task.id)
        try:
            http_post(
                url=f"{self.url}/task/cancel",
                json={"task_id": task.id},
            )
            self.log_info("cancelling task: finished", task_id=task.id)
        except Exception as e:
            self.log_error("cancelling task: failed", task_id=task.id, error=e)
            raise e

    def cancel_all(self):
        self.log_info("cancelling all tasks: started")
        try:
            http_post(
                url=f"{self.url}/task/cancel_all",
                json={},
            )
            self.log_info("cancelling all tasks: finished")
        except Exception as e:
            self.log_error("cancelling all tasks: failed", error=e)
            raise e

    def status(self, task: Task) -> str:
        self.log_info("getting task status: started", task_id=task.id)
        try:
            response = http_get(
                url=f"{self.url}/task/status",
                json={"task_id": task.id},
            )
            task_status = "undefined"
            if response:
                task_status = response.json().get("task_status", task_status)
            self.log_info(
                "getting task status: finished",
                task_id=task.id,
                task_status=task_status,
            )
            return task_status
        except Exception as e:
            self.log_error("getting task status: failed", task_id=task.id, error=e)
            raise e
