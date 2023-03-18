from __future__ import annotations

import json
import uuid
from typing import Dict, Any, Optional


class Task:
    def __init__(self, topic: str, payload: str, task_id: Optional[str] = None):
        self.__id = task_id or str(uuid.uuid4())
        self.__topic = topic
        self.__payload = json.loads(payload)

    @property
    def id(self) -> str:
        return self.__id

    @property
    def topic(self) -> str:
        return self.__topic

    @property
    def payload(self) -> Dict[str, Any]:
        return self.__payload

    def get_json_to_export(self):
        return {
            "id": self.id,
            "topic": self.topic,
            "payload": json.dumps(self.payload),
        }

    @classmethod
    def deserialize(cls, task_data: Dict[str, Any]) -> Task:
        return Task(
            topic=task_data["topic"],
            payload=task_data["payload"],
            task_id=task_data["id"],
        )
