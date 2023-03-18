import abc

from bachelor_core.application.application import Application
from bachelor_core.common.logging.loggable import Loggable


class BaseWrapper(Loggable, abc.ABC):
    def __init__(self, app: Application, wrapped_app_name: str):
        Loggable.__init__(self, app.NAME, f"{wrapped_app_name}_wrapper")

        self.__app = app

    @property
    def app(self) -> Application:
        return self.__app
