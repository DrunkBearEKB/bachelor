from __future__ import annotations

import abc
import traceback
from typing import Dict, Any

from bachelor_core.application.application import Application
from bachelor_core.common.logging.loggable import Loggable


class BasePlugin(abc.ABC, Loggable):
    """
    Базовый плагин
    """

    NAME = None
    PLUGIN_INSTALL = []

    _plugin_obj = None

    def __init__(self, app: Application, config: Dict[str, Any]):
        super().__init__(app.NAME, f"{app.NAME}.{self.NAME}")
        self.__app = app
        self.__config = config

        BasePlugin._plugin_obj = self

    @classmethod
    def install(cls, app: Application, config: Dict[str, Any]):
        """
        Установка плагина в приложение

        Args:
            app (Application): Приложение
            config (Dict[str, Any]): Конфиг плагина

        Returns:

        """
        name = cls.NAME or cls.__name__
        try:
            plugin = cls(app, config)
            attr_name = name
            setattr(app, attr_name, plugin)
            for attr_name in cls.PLUGIN_INSTALL:
                setattr(app, attr_name, getattr(plugin, attr_name))

            cls.get().log_info(f"{name} installed to {app.__class__.__name__}")

        except Exception as e:
            cls.get().log_info(f"failed to initialize {name}: {e}")
            traceback.print_exception(e)

    @classmethod
    def get(cls) -> BasePlugin:
        return cls._plugin_obj

    @property
    def _app(self) -> Application:
        return self.__app

    @property
    def _config(self) -> Dict[str, Any]:
        return self.__config
