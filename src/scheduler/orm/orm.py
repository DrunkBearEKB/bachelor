from sqlalchemy import Column, Integer, String

from bachelor_core.common.utils.dbhelper import BaseModel


class TaskStatus:
    NOT_STARTED = "not started"
    STARTED = "started"
    DONE = "done"
    FAILED = "failed"
    CANCELED = "canceled"


class Task(BaseModel):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    topic = Column(String(64), nullable=False)
    payload = Column(String(1024), nullable=False)
    start_dt = Column(String(64), nullable=False)
    finish_dt = Column(String(64), nullable=False)
    status = Column(String(64), nullable=False)

    def get_json_to_export(self):
        return {
            "id": self.id,
            "topic": self.topic,
            "payload": self.payload,
        }

    def __repr__(self) -> str:
        return (
            f"Task("
            f"id={self.id},"
            f"topic={self.topic},"
            f"payload={self.payload},"
            f"start_dt={self.start_dt},"
            f"finish_dt={self.finish_dt},"
            f"status={self.status},"
            f")"
        )
