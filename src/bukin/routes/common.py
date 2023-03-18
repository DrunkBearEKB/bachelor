import flask

from bachelor_core.application.application import get_application
from bachelor_core.application.flask.flask_routes import FlaskRoutes
from bachelor_core.application.plugins.secrets import get_value_from_secrets


DEFAULT_REDIRECT_URL = "/bukin/?info=description"


def get_header_by_section(section: str) -> str:
    return {
        "description": "Description",
        "references": "References",
        "gateway": "Gateway",
        "scheduler": "Scheduler",
        "worker": "Worker",
        "databroker": "DataBroker",
        "candace": "Candace",
        "tvm": "TVM",
        "static": "Static",
        "dynamic": "Dynamic",
        "new_release": "New Release",
        "rollback": "Rollback",
    }[section]


class BukinCommonRoutes(FlaskRoutes):
    @classmethod
    def add_routes(cls, flask_app: flask.Flask):
        @flask_app.route("/bukin/", methods=["GET"])
        def get_bukin_main():
            info = flask.request.args.get("info", "")
            app = flask.request.args.get("app", "")
            config = flask.request.args.get("config", "")
            deploy = flask.request.args.get("deploy", "")

            if not info and not app and not config and not deploy:
                return flask.redirect(DEFAULT_REDIRECT_URL)

            section = None
            if info in ["description", "references"]:
                section = info
            elif app in [
                "gateway", "scheduler", "worker", "databroker", "candace", "tvm"
            ]:
                section = app
            elif config in ["static", "dynamic"]:
                section = config
            elif deploy in ["new_release", "rollback"]:
                section = deploy

            if section:
                title = f"Bukin | {get_header_by_section(section)}"
                page = f"bukin_{section}.html"
            else:
                title = "Bukin"
                page = "bukin.html"

            app = get_application()
            monitoring_component = app.config_components.get("bukin_monitorings")
            monitoring_link_vm = get_value_from_secrets(
                monitoring_component.get("vm")
            )
            monitoring_link_services = get_value_from_secrets(
                monitoring_component.get("services")
            )
            monitoring_link_pg = get_value_from_secrets(
                monitoring_component.get("pg")
            )
            return flask.render_template(
                page,
                **{
                    "title": title,
                    "section": section,
                    "monitoring_link_vm": monitoring_link_vm,
                    "monitoring_link_services": monitoring_link_services,
                    "monitoring_link_pg": monitoring_link_pg,
                }
            )
