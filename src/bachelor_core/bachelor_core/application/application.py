from __future__ import annotations

import abc
import json
import os.path
import sys
from typing import Optional, Dict, Any

from bachelor_core.common.logging.loggable import Loggable
from bachelor_core.application.application_errors import (
    ApplicationError,
    ApplicationConfigError,
)
from bachelor_core.common.utils.imports import resolve

PATH_CONFIG_DEFAULT = "../../configs/static.cfg.json"


class Application(Loggable, abc.ABC):
    """
    Базовое приложение
    """

    NAME = None
    VERSION = None

    _app_obj = None

    def __init__(self, path_config: Optional[str] = None):
        Loggable.__init__(self, self.NAME)

        self.log_info("#################### Starting Application ####################")
        self.log_info(f"Application constructor called with {path_config=}")

        if self.NAME is None:
            raise ApplicationError("Application NAME is not specified!")
        if self.VERSION is None:
            raise ApplicationError("Application VERSION is not specified!")

        self.log_info(f"Starting {self.NAME} ver {self.VERSION}")

        self.__path_config = os.path.join(
            os.path.dirname(sys.argv[0]), path_config or PATH_CONFIG_DEFAULT
        )
        if not os.path.exists(self.__path_config):
            raise ApplicationConfigError(
                f"can not find config file: {self.__path_config}!"
            )

        Application._app_obj = self

        self.__load_configs()
        self.__install_plugins()

    def run(self):
        """
        Запуск приложения
        """
        pass

    def __recursive_import_all(self):
        pass

    def __load_configs(self):
        """
        Загрузка конфигов
        """
        with open(self.__path_config, mode="r") as file_config:
            content = json.load(file_config)

        if self.NAME not in content["servants"]:
            raise ApplicationConfigError(f"can not load config data for {self.NAME}!")
        self.__full_config = content
        self.__config = content["servants"][self.NAME]
        self.__config_components = content["components"]

    def __install_plugins(self):
        """
        Установка плагинов
        """
        plugins = self.__config.get("plugins", {})
        for plugin_cls_path, plugin_config in plugins.items():
            cls = resolve(plugin_cls_path)
            cls.install(self, plugin_config)

    @property
    def config(self) -> Dict[str, Any]:
        """
        Returns:
            Dict[str, Any]: Конфигурационные данные приложения
        """
        return self.__config

    @property
    def config_components(self) -> Dict[str, Any]:
        """
        Returns:
            Dict[str, Any]: Конфигурационные данные компонент
        """
        return self.__config_components

    def get_app_config(self, app_name: str) -> Dict[str, Any]:
        """
        Returns:
            Dict[str, Any]: Конфигурационные данные
        """
        if not app_name:
            app_name = self.NAME
        return self.__full_config["servants"][app_name]

    @classmethod
    def get(cls) -> Application:
        """
        Returns:
            Application: Текущее инициализированное приложение
        """
        return cls._app_obj


def get_application() -> Application:
    """
    Returns:
        Application: Текущее инициализированное приложение
    """
    return Application.get()
