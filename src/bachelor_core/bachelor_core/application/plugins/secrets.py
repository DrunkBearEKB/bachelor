from typing import Dict, Any

from bachelor_core.application.application import Application
from bachelor_core.application.base_plugin import BasePlugin
from bachelor_core.common.utils.config_helper import ConfigHelper

import psycopg2


class SecretsPlugin(BasePlugin):
    """
    Плагин для использования секретов
    """

    NAME = "secrets"
    PLUGIN_INSTALL = [
        "get_value",
    ]

    DEFAULT_SECRETS_FILENAME = "./configs/secrets.json"

    def __init__(self, app: Application, config: Dict[str, Any]):
        super().__init__(app, config)

        self.__cfg_filename = config.get("filename", self.DEFAULT_SECRETS_FILENAME)

    def get_value(self, key: str) -> Any:
        self.log_info("getting secret: started", key=key)
        try:
            value = ConfigHelper(self.__cfg_filename).get(key, None)
            self.log_info("getting secret: finished", key=key)
            return value
        except Exception as e:
            self.log_error("getting secret: failed", key=key, error=e)
            raise


def get_value_from_secrets(key: str) -> Any:
    app = Application.get()
    if hasattr(app, "secrets"):
        return app.secrets.get_value(key)
    return None
