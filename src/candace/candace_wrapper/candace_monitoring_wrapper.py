import socket
from typing import Dict, Any

from bachelor_core.application.application import Application
from bachelor_core.application.wrapper.base_rest_wrapper import BaseRESTWrapper
from bachelor_core.common.http.requests import http_post


class CandaceMonitoringWrapper(BaseRESTWrapper):
    def __init__(self, app: Application):
        BaseRESTWrapper.__init__(self, app, "candace", "candace/monitoring")

    def send_monitoring_metric(
        self, sensor: str, labels: Dict[str, Any], forward: bool = False
    ):
        labels.update(
            {
                "host": socket.gethostname(),
                "app": self.app.NAME,
                "sensor": str(sensor),
            }
        )

        self.log_info("sending monitoring metric: started")
        try:
            http_post(
                url=f"{self.url}/write?forward={forward}",
                json={"labels": labels},
            )
            self.log_info("sending monitoring metric: finished")
        except Exception as e:
            self.log_error("sending monitoring metric: failed", error=e)
            raise e
