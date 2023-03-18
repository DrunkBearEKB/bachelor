import flask

from http import HTTPStatus

from bachelor_core.application.flask.flask_routes import FlaskRoutes


class SchedulerCommonRoutes(FlaskRoutes):
    @classmethod
    def add_routes(cls, flask_app: flask.Flask):
        @flask_app.route("/scheduler/ping", methods=["GET"])
        def get_scheduler_ping():
            return flask.jsonify({}), HTTPStatus.OK

        @flask_app.route("/scheduler/pingdb", methods=["GET"])
        def get_scheduler_pingb():
            return flask.jsonify({}), HTTPStatus.OK
