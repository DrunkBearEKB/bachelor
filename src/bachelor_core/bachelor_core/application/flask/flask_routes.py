import abc

import flask


class FlaskRoutes(abc.ABC):
    """
    Базовый класс для определения путей, обрабатываемых приложением
    """

    @classmethod
    @abc.abstractmethod
    def add_routes(cls, app: flask.Flask):
        """
        Добавление объявленных внутри функции путей

        Args:
            app (flask.Flask): Приложение
        """
        raise NotImplementedError()
