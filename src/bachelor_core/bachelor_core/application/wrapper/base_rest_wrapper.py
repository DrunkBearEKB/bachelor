import abc

from bachelor_core.application.application import Application
from bachelor_core.application.wrapper.base_wrapper import BaseWrapper


class BaseRESTWrapper(BaseWrapper, abc.ABC):
    def __init__(self, app: Application, wrapped_app_name: str, url: str):
        BaseWrapper.__init__(self, app, wrapped_app_name)

        self.__app = app
        wrapped_app_config = app.get_app_config(wrapped_app_name)
        port = wrapped_app_config.get("launch", {}).get("port", 80)
        self.__url = f"http://localhost:{port}/{url}"

    @property
    def app(self) -> Application:
        return self.__app

    @property
    def url(self) -> str:
        return self.__url
