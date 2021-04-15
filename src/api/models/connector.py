from __future__ import annotations

import builtins
import sys
from types import TracebackType
from typing import Callable, Dict, Optional, Sequence, Type, Union

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session, sessionmaker
from typing_extensions import Literal

import settings as se


"""
    @author: Jaroslav Kirichok
    @authors: Delete this text-line if you work with the code below
              and write your name
    @license: GNU GENERAL PUBLIC LICENSE 3
"""


__all__: Sequence[str] = ('DatabaseConnector',)


class DatabaseConnector(builtins.object):

    enter_to_context = property(lambda self: self._enter_to_context)  # return bool
    session = property(lambda self: self._session)  # return ScopedSession

    def __init__(
        self, engine_type: se.DatabaseEngines, credentials: Dict[str, Union[int, str]] = {}
    ) -> None:
        """Creates SQLAlchemy session object from default.properties config file
        that storage in shared.file_vars object settings.py.

        Args:
            engine: Database engine(dbms) in the string form (example: mysql+...,
                    posgtresql, etc.) can be taken or supplemented required in the
                    class DatabaseEngines (example: DatabaseEngines.MYSQL.value)
            credentials: Configs from *.properties file
        """
        self._enter_to_context = True
        # Database connection credentials
        self._db_name = credentials.get('db_name')
        self._engine_type = engine_type
        self._host = credentials.get('db_host')
        self._port = credentials.get('db_port')
        self._pwd = credentials.get('db_password')
        self._user = credentials.get('db_user')

    def __enter__(self) -> DatabaseConnector:
        suitable_connector: Callable[..., None] = {
                se.DatabaseEngines.MYSQL:
                        lambda: create_engine(
                                    f'{self._engine_type.value}://{self._user}:{self._pwd}@{self._host}:{self._port}/{self._db_name}',
                                    connect_args={'connect_timeout': se.shared.DB_CONNECT_TIMEOUT}),
                se.DatabaseEngines.SQLITE:
                        lambda: create_engine(f'{self._engine_type.value}:///{se.shared.EXTRAS_DIR}/employees.sqlite3')
        }.get(self._engine_type, lambda: None)
        # ... and call loader function
        self._engine = suitable_connector()
        try:
            # After creating the engine based on the launch mode, try
            # to connect to the database
            self._session = None
            self._engine.connect()
            # If the connection is successful - create a session and return it
            Scoped_Session = \
                scoped_session(sessionmaker(autoflush=False, bind=self._engine))
            self._session = Scoped_Session()
        except SQLAlchemyError:
            if self.__exit__(*sys.exc_info()):
                self._enter_to_context = False
            else:
                raise
        return self

    def __exit__(self,
                 exc_type:  Optional[Type[BaseException]],
                 exc_value: Optional[BaseException],
                 exc_trace: Optional[TracebackType]
    ) -> Literal[True]:
        try:
            if self._session:
                self._session.close()
        except SQLAlchemyError:
            se.logger.error(
                f'Failure SQLAlchemy: {self._host} : {self._port}', exc_info=True)
        finally:
            return True
