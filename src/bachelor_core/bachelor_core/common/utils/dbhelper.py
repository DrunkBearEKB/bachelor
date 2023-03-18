from typing import Set, Type

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from bachelor_core.application.application import get_application
from bachelor_core.application.plugins.secrets import get_value_from_secrets
from bachelor_core.common.utils.imports import resolve
from bachelor_core.common.utils.subclasses import get_all_subclasses

BaseModel = declarative_base()


class DBHelper:
    def __init__(self, db_id: str):
        app = get_application()
        db_component = app.config_components.get(db_id, {})

        user = get_value_from_secrets(db_component.get("user"))
        password = get_value_from_secrets(db_component.get("password"))
        host = get_value_from_secrets(db_component.get("host"))
        port = get_value_from_secrets(db_component.get("port"))
        database = db_component.get("database")
        uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

        engine = create_engine(uri)

        BaseModel.metadata.create_all(engine)
        self.__session = sessionmaker(bind=engine)()

        exec("from orm.orm import *")  # TODO: remove using this (VERY BAD)
        for cls in self.__find_defined_orm_models():
            resolve(f"{cls.__module__}.{cls.__name__}")

        BaseModel.metadata.create_all(engine)
        self.__db_id = db_id

    @staticmethod
    def __find_defined_orm_models() -> Set[Type[BaseModel]]:
        return get_all_subclasses(BaseModel)

    @property
    def session(self) -> Session:
        return self.__session

    def commit(self):
        return self.__session.commit()

    @property
    def db_id(self) -> str:
        return self.__db_id
