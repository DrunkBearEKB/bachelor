import json
from typing import Any


class ConfigHelper:
    def __init__(self, filename: str):
        self.__filename = filename

    def get(self, key: str, default_value=None) -> Any:
        config = self.__read()
        return config.get("vars", {}).get(key, default_value)

    def __read(self):
        with open(self.__filename) as file:
            config = json.load(file)
        return config
