from typing import Dict, Any

from bachelor_core.application.base_plugin import BasePlugin
from bachelor_core.application.application import Application
from bachelor_core.common.utils.config_helper import ConfigHelper


class DynamicCfgPlugin(BasePlugin):
    """
    Плагин для использования динамического конфига
    """

    NAME = "dynamic_cfg"
    PLUGIN_INSTALL = [
        "get_var",
    ]

    DEFAULT_CFG_FILENAME = "./configs/dynamic.cfg.json"

    def __init__(self, app: Application, config: Dict[str, Any]):
        super().__init__(app, config)

        self.__cfg_filename = config.get("filename", self.DEFAULT_CFG_FILENAME)

    def get_var(self, key: str, default_value=None) -> Any:
        self.log_info("getting variable: started", key=key, default_value=default_value)
        try:
            value = ConfigHelper(self.__cfg_filename).get(key, default_value)
            self.log_info("getting variable: finished", key=key, value=value)
            return value
        except Exception as e:
            self.log_error("getting variable: failed", key=key, error=e)
            raise


def get_var_from_dynamic_cfg(key: str, default_value=None) -> Any:
    app = Application.get()
    if hasattr(app, "dynamic_cfg"):
        return app.dynamic_cfg.get_var(key, default_value)
    return None
