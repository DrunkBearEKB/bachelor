import flask
from http import HTTPStatus

from bachelor_core.common.utils.datetime import get_current_datetime_str
from orm.orm import Task, TaskStatus

from bachelor_core.application.application import get_application
from bachelor_core.application.flask.flask_routes import FlaskRoutes
from bachelor_core.common.utils.dbhelper import DBHelper


class SchedulerTaskRoutes(FlaskRoutes):
    @classmethod
    def add_routes(cls, flask_app: flask.Flask):
        @flask_app.route("/scheduler/task/enqueue", methods=["POST"])
        def post_scheduler_task_enqueue():
            dbhelper: DBHelper = get_application().dbhelper

            if not flask.request.is_json:
                return flask.jsonify(
                    {
                        "message": "no JSON data received"
                    }
                ), HTTPStatus.BAD_REQUEST

            data = flask.request.json

            task_data = data.get("task", None)
            if not task_data:
                return flask.jsonify(
                    {
                        "message": "the required `task` argument was not passed"
                    }
                ), HTTPStatus.BAD_REQUEST

            task_topic = task_data.get("topic", None)
            if not task_topic:
                return flask.jsonify(
                    {
                        "message": "the required `task.topic` argument was not passed"
                    }
                ), HTTPStatus.BAD_REQUEST

            task_payload = task_data.get("payload", None)
            if not task_payload:
                return flask.jsonify(
                    {
                        "message": "the required `task.payload` argument was not passed"
                    }
                ), HTTPStatus.BAD_REQUEST

            task = Task(
                topic=task_topic,
                payload=task_payload,
                start_dt="",
                finish_dt="",
                status=TaskStatus.NOT_STARTED,
            )
            dbhelper.session.add(task)
            dbhelper.commit()

            return flask.jsonify(
                {
                    "task_id": task.id,
                }
            ), HTTPStatus.OK

        @flask_app.route("/scheduler/task/get", methods=["GET"])
        def get_scheduler_task_get():
            dbhelper: DBHelper = get_application().dbhelper

            if not flask.request.is_json:
                return flask.jsonify(
                    {
                        "message": "no JSON data received"
                    }
                ), HTTPStatus.BAD_REQUEST

            data = flask.request.json

            topics = data.get("topics", [])

            task = (
                dbhelper
                .session
                .query(Task)
                .filter(
                    Task.status == TaskStatus.NOT_STARTED,
                    Task.topic.in_(topics),
                    Task.start_dt <= get_current_datetime_str(),
                )
                .first()
            )
            if task:
                task.start_dt = get_current_datetime_str()
                task.status = TaskStatus.STARTED
                dbhelper.commit()
                return flask.jsonify(
                    {
                        "task": task.get_json_to_export(),
                    }
                ), HTTPStatus.OK

            task = (
                dbhelper
                .session
                .query(Task)
                .filter(
                    Task.status == TaskStatus.NOT_STARTED,
                    Task.topic.in_(topics),
                )
                .first()
            )

            if task:
                task.start_dt = get_current_datetime_str()
                task.status = TaskStatus.STARTED
                dbhelper.commit()
                return flask.jsonify(
                    {
                        "task": task.get_json_to_export(),
                    }
                ), HTTPStatus.OK

            return flask.jsonify(
                {
                    "task": {},
                },
            ), HTTPStatus.OK

        @flask_app.route("/scheduler/task/done", methods=["POST"])
        def post_scheduler_task_done():
            dbhelper: DBHelper = get_application().dbhelper

            if not flask.request.is_json:
                return flask.jsonify(
                    {
                        "message": "no JSON data received"
                    }
                ), HTTPStatus.BAD_REQUEST

            data = flask.request.json

            task_id = data.get("task_id", None)
            if not task_id:
                return flask.jsonify(
                    {
                        "message": "the required `task_id` argument was not passed"
                    }
                ), HTTPStatus.BAD_REQUEST

            task = (
                dbhelper
                .session
                .query(Task)
                .filter_by(id=task_id)
                .first()
            )
            if not task:
                return flask.jsonify(
                    {
                        "message": f"task with id={task_id} not found"
                    }
                ), HTTPStatus.NOT_FOUND

            task.finish_dt = get_current_datetime_str()
            task.status = TaskStatus.DONE
            dbhelper.commit()

            return flask.jsonify(
                {
                    "message": "task successfully updated"
                }
            ), HTTPStatus.OK

        @flask_app.route("/scheduler/task/failed", methods=["POST"])
        def post_scheduler_task_failed():
            dbhelper: DBHelper = get_application().dbhelper

            if not flask.request.is_json:
                return flask.jsonify(
                    {
                        "message": "no JSON data received"
                    }
                ), HTTPStatus.BAD_REQUEST

            data = flask.request.json

            task_id = data.get("task_id", None)
            if not task_id:
                return flask.jsonify(
                    {
                        "message": "the required `task_id` argument was not passed"
                    }
                ), HTTPStatus.BAD_REQUEST

            task = (
                dbhelper
                .session
                .query(Task)
                .filter_by(id=task_id)
                .first()
            )
            if not task:
                return flask.jsonify(
                    {
                        "message": f"task with id={task_id} not found"
                    }
                ), HTTPStatus.NOT_FOUND

            task.finish_dt = get_current_datetime_str()
            task.status = TaskStatus.FAILED
            dbhelper.commit()

            return flask.jsonify(
                {
                    "message": "task successfully updated"
                }
            ), HTTPStatus.OK

        @flask_app.route("/scheduler/task/cancel", methods=["POST"])
        def post_scheduler_task_cancel():
            dbhelper: DBHelper = get_application().dbhelper

            if not flask.request.is_json:
                return flask.jsonify(
                    {
                        "message": "no JSON data received"
                    }
                ), HTTPStatus.BAD_REQUEST

            data = flask.request.json

            task_id = data.get("task_id", None)
            if not task_id:
                return flask.jsonify(
                    {
                        "message": "the required `task_id` argument was not passed"
                    }
                ), HTTPStatus.BAD_REQUEST

            task = (
                dbhelper
                .session
                .query(Task)
                .filter_by(id=task_id)
                .first()
            )
            if not task:
                return flask.jsonify(
                    {
                        "message": f"task with id={task_id} not found"
                    }
                ), HTTPStatus.NOT_FOUND

            task.finish_dt = get_current_datetime_str()
            task.status = TaskStatus.CANCELED
            dbhelper.commit()

            return flask.jsonify(
                {
                    "message": "task successfully updated"
                }
            ), HTTPStatus.OK

        @flask_app.route("/scheduler/task/cancel_all", methods=["POST"])
        def post_scheduler_task_cancel_all():
            dbhelper: DBHelper = get_application().dbhelper

            tasks = (
                dbhelper
                .session
                .query(Task)
            )
            counter = 0
            counter_commit = 50
            for task in tasks:
                task.finish_dt = get_current_datetime_str()
                task.status = TaskStatus.CANCELED
                counter += 1

                if counter >= counter_commit:
                    dbhelper.commit()
                    counter = 0
            dbhelper.commit()

            return flask.jsonify(
                {
                    "message": "no JSON data received"
                }
            ), HTTPStatus.BAD_REQUEST

        @flask_app.route("/scheduler/task/status", methods=["GET"])
        def get_scheduler_task_status():
            dbhelper: DBHelper = get_application().dbhelper

            if not flask.request.is_json:
                return flask.jsonify(
                    {
                        "error": "no JSON data received"
                    }
                ), HTTPStatus.BAD_REQUEST

            data = flask.request.json

            task_id = data.get("task_id", None)
            if not task_id:
                return flask.jsonify(
                    {
                        "message": "the required `task_id` argument was not passed"
                    }
                ), HTTPStatus.BAD_REQUEST

            task = (
                dbhelper
                .session
                .query(Task)
                .filter_by(id=task_id)
                .first()
            )
            if not task:
                return flask.jsonify(
                    {
                        "message": f"task with id={task_id} not found"
                    }
                ), HTTPStatus.NOT_FOUND

            return flask.jsonify(
                {
                    "task_status": task.status
                }
            ), HTTPStatus.OK
