import abc
import decimal
import time
import traceback
import uuid
from typing import Optional
from flask import Flask, request, Response, render_template, g as requests_globals
import logging

from bachelor_core.application.application import Application, get_application

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)


class FlaskApplication(Application, abc.ABC):
    """
    Базовое приложение для всех приложений основанных на Flask
    """

    def __init__(self):
        Application.__init__(self)

        self.__flask_app = Flask(self.NAME)

    @property
    def flask_app(self) -> Flask:
        return self.__flask_app

    @abc.abstractmethod
    def _add_routes(self):
        raise NotImplementedError()

    def _before_request(self):
        pass

    def _after_request(self, response: Response):
        pass

    def _handle_error(self, error: Exception, http_status_code: int):
        pass

    def run(self):
        super().run()

        @self.flask_app.before_request
        def before_request():
            request_id = str(uuid.uuid4())
            requests_globals.start = time.time()
            requests_globals.request_id = request_id

            params = f" params: {request.json}" if request.is_json else ""
            if request.endpoint:
                self.log_info(
                    f"request "
                    f"{request.method} "
                    f"{request.url_rule} "
                    f"{self.NAME}.{request.endpoint} "
                    f"started "
                    f"{params}",
                    request_id=request_id,
                )
                self.log_info(
                    f"request headers: {dict(request.headers)}",
                    request_id=request_id,
                )
            else:
                self.log_info(
                    f"{request.method} "
                    f"/{request.url.replace(request.url_root, '')} not found"
                    f"{params}",
                    request_id=request_id,
                )
            self._before_request()

        @self.flask_app.after_request
        def after_request(response: Response):
            request_id = requests_globals.request_id

            if request.endpoint:
                time_diff = round(
                    decimal.Decimal(time.time() - requests_globals.start), 3
                )
                if response.is_json:
                    self.log_info(
                        f"{self.NAME}.{request.endpoint} "
                        f"response: {response.json}",
                        request_id=request_id,
                    )
                self.log_info(
                    f"{request.method} "
                    f"{request.url_rule} "
                    f"took {time_diff} sec, "
                    f"status: {response.status}",
                    request_id=request_id,
                )
            self._after_request(response)
            return response

        @self.flask_app.errorhandler(Exception)
        def handle_error(error: Exception):
            if hasattr(error, "code"):
                code = error.code
                description = str(error)
            else:
                code = 500
                description = f"{code} Internal server error: {str(error)}"
            self._handle_error(error, code)
            try:
                return render_template(
                    "error.html",
                    title=f"Exception {code}",
                    error_code=code,
                    error_description=description,
                    error_lines=traceback.format_exc().split("\n"),
                ), code
            except:
                return {
                    "error": f"Exception {code}",
                    "description": description,
                    "error_lines": traceback.format_exc().split("\n"),
                }, code

        self._add_routes()
        self.__flask_app.config["TRAP_HTTP_EXCEPTIONS"] = True
        port = self.config.get("launch", {}).get("port", 80)
        self.__flask_app.run(host="0.0.0.0", port=port)


def get_flask_application_if_possible() -> Optional[FlaskApplication]:
    app = get_application()
    if isinstance(app, FlaskApplication):
        return app
    return None
