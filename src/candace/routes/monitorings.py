import flask
import requests
from typing import Dict, Any

from bachelor_core.application.application import get_application
from bachelor_core.application.flask.flask_routes import FlaskRoutes
from bachelor_core.application.plugins.secrets import get_value_from_secrets
from bachelor_core.common.auth.iam import get_iam_token
from bachelor_core.common.http.requests import http_post


def write_metrics(labels: Dict[str, Any]) -> requests.Response:
    app = get_application()
    folder_id = get_value_from_secrets(
        app.config_components.get("yandex_monitoring", {}).get("folder_id")
    )
    iam_token = get_iam_token()

    return http_post(
        f"https://monitoring.api.cloud.yandex.net/monitoring/v2/data/write?"
        f"folderId={folder_id}&service=custom",
        json={
            # "ts": datetime.datetime.now().isoformat(),
            "metrics": [
                {
                    "name": "bachelor",
                    "labels": labels,
                    "type": "DGAUGE",
                    "value": 1,

                }
            ]
        },
        headers={
            "Authorization": f"Bearer {iam_token}",
            "Content-Type": "application/json",
        }
    )


class CandaceMonitoringRoutes(FlaskRoutes):
    @classmethod
    def add_routes(cls, flask_app: flask.Flask):
        @flask_app.route("/candace/monitoring/write", methods=["POST"])
        def post_candace_write():
            forward = flask.request.args.get("forward")
            labels = flask.request.json.get("labels")

            if forward:
                result = write_metrics(labels)
                if result:
                    return {
                        "status": "success",
                        "result": result.json(),
                    }, 200

            return {
                "status": "success",
            }
