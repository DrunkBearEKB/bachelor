from bachelor_core.application.flask.flask_application import FlaskApplication
from routes.monitorings import CandaceMonitoringRoutes


class Candace(FlaskApplication):
    NAME = "candace"
    VERSION = "0.0.1"

    def __init__(self):
        FlaskApplication.__init__(self)

    def _add_routes(self):
        routes_group = [CandaceMonitoringRoutes]
        for routes in routes_group:
            routes.add_routes(self.flask_app)


if __name__ == "__main__":
    app = Candace()
    app.run()
