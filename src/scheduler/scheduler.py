from flask import Response, request

from routes.common import SchedulerCommonRoutes
from routes.task import SchedulerTaskRoutes

from bachelor_core.application.flask.flask_application import FlaskApplication
from candace_wrapper.candace_monitoring_wrapper import CandaceMonitoringWrapper


class Scheduler(FlaskApplication):
    NAME = "scheduler"
    VERSION = "0.0.1"

    def __init__(self):
        FlaskApplication.__init__(self)

        self.__candace = CandaceMonitoringWrapper(self)

    def _after_request(self, response: Response):
        self.__candace.send_monitoring_metric(
            request.path,
            {
                "http_status_code": str(response.status_code),
                "status": "Success",
            },
            forward=True,
        )

    def _handle_error(self, error: Exception, http_status_code: int):
        self.__candace.send_monitoring_metric(
            request.path,
            {
                "http_status_code": str(http_status_code),
                "status": error.__class__.__name__,
            },
            forward=True,
        )

    def _add_routes(self):
        routes_group = [SchedulerCommonRoutes, SchedulerTaskRoutes]
        for routes in routes_group:
            routes.add_routes(self.flask_app)


if __name__ == "__main__":
    app = Scheduler()
    app.run()
