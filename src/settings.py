import argparse
import builtins
import collections
import configparser
import json
import logging
import sys
from enum import Enum
from os import path
from types import MappingProxyType
from typing import (
    Any,
    Callable,
    ChainMap,
    Dict,
    Mapping,
    Optional,
    Sequence,
    TypeVar,
    Union,
    cast,
)

from pendulum import now

import helpers


"""
    @author: Jaroslav Kirichok
    @authors: Delete this text-line if you work with the code below
              and write your name
    @license: GNU GENERAL PUBLIC LICENSE 3
"""


__all__: Sequence[str] = ('DatabaseEngines', 'logger', 'shared')

# Types definitions
SharedType = TypeVar('SharedType')


class SharedValuesMeta(builtins.type):
    # A metaclass that creates a Singleton base class
    # when called
    def __init__(cls, *args: Any, **kwargs: Any) -> None:
        """Singleton SharedValuesMeta for the keep setting up vars the application.

        Args:
            args: To pass an unknown number of unnamed arguments
            kwargs: To pass an unknown number of named arguments
        """
        cls._instance = None
        cls.get_instance = classmethod(lambda classable: classable._instance)
        # ...and call parent __init__
        super().__init__(*args, **kwargs)

    def __call__(cls, *args: Any, **kwargs: Any) -> Optional[SharedType]:
        if not cls._instance:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class SharedValues(metaclass=SharedValuesMeta):
    """Class with overloaded internal protocol descriptors giving
    easy access to common project constants.
    """
    def __setattr__(self, name: str, value: Any) -> None:
        try:
            self.__dict__[name] = value
        except KeyError:
            raise AttributeError(
                        '__setattr__() in class SharedValues failed.')

    def __getattr__(self, name: str) -> Any:  # not good, but this is the most acceptable option
        try:
            return self.__dict__[name]
        except KeyError:
            raise AttributeError(
                        '__getattr__() in class SharedValues failed.')

    def __delattr__(self, name: str) -> None:
        if self.__dict__.get(name):
            raise AttributeError(
                        '__delattr__() it is forbidden to delete attributes.')


class ExtraFileVars(builtins.object):
    """Class that reads data from *.properties, *.json or any
    other *.* configuration files.
    """
    def __init__(self) -> None:
        """When typing JSON there is no final decision yet. This is
        best solution so far. See more at issue: https://github.com/python/typing/issues/182
        """
        self._chain_map: \
            ChainMap[str, Mapping[str, Any]] = collections.ChainMap({'default': {}})

    def pluck(self, caption: str = '') -> Mapping[str, Any]:
        """Takes a specific node from the "store" by its name/caption. If the
        host name is not passed, the entire settings ``store`` is returned.

        Args:
            caption: Node aka ChainMap, what you need to return/receive

        Returns:
            ``Node`` or ``None`` storage with the read-only permissions.
        """
        claim_setting_vars = self._chain_map.get(caption)
        if claim_setting_vars is None:
            return MappingProxyType({})
        # ...otherwise, return read vars
        return MappingProxyType(claim_setting_vars)

    def load(self, caption: str, file_path: str) -> None:
        """A very simple function that calls the relevant extension
        function. Something like a design pattern ``Strategy`` or ``Visitor``.

        Args:
            caption: Key name in ChainMap (see: ``self._chain_map``)
            file_path: Path to the file with configs
        """
        *_, file_ext = path.splitext(file_path)
        suitable_file_loader: Callable[..., None] = {
                '.properties':
                    lambda: self.properties_file(caption, file_path),
                '.json':
                    lambda: self.json_file(caption, file_path)
        }.get(file_ext, lambda: None)
        # ... and call loader function
        suitable_file_loader()

    @helpers.disallow
    def properties_file(self, caption: str, file_path: str) -> None:
        """Reads configs from *.properties files of ``extras`` directory.

        Args:
            caption: Key name in the ChainMap (see: ``self._chain_map``)
            file_path: Path to the file with configs
        """
        with open(file_path, 'r') as fl:
            parser = configparser.ConfigParser()
            parser.read_file(fl)
            setting_vars: Dict[str, Union[str, int]] = {}
            for section in parser.sections():
                setting_vars.update(cast(Dict[str, Union[str, int]],
                                         parser.items(section)))
            self._chain_map.update({caption: setting_vars})

    @helpers.disallow
    def json_file(self, caption: str, file_path: str) -> None:
        """A very simple function that reads configs from *.json
        files of ``extras`` directory.

        Args:
            caption: Key name in the ChainMap
            file_path: Path to the file with configs
        """
        with open(file_path, 'r') as r_fl:
            self._chain_map.update({caption: json.load(r_fl)})


class NoValue(Enum):

    def __repr__(self) -> str:
        return '<%s.%s>' % (self.__class__.__name__, self.name)


class DatabaseEngines(NoValue):
    """Enum for the agregate database engine names. Can be taken or
    supplemented required in class DatabaseEngines.

    Example: DatabaseEngines.MYSQL.value returns str 'mysql+mysqlconnector'
    """
    # Installation required mysqlconnector
    # See more: https://pypi.org/project/mysql-connector-python/
    MYSQL = 'mysql+mysqlconnector'
    # See more: https://docs.sqlalchemy.org/en/13/dialects/sqlite.html
    SQLITE = 'sqlite'


parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-r', '--release',
                    action='store_true',
                    help='run server in release mode')
cli_args = parser.parse_args()

shared = SharedValues()

# Application manual config
#
# Debug or release
shared.DEBUG = not cli_args.release or False

# Server vars
shared.HOST, shared.PORT = '0.0.0.0', 9000

# Path dir vars
shared.BASE_DIR = path.dirname(path.realpath(__file__))
shared.EXTRAS_DIR = path.join(shared.BASE_DIR, 'extras')
shared.LOGS_DIR = path.join(shared.BASE_DIR, 'logs')
shared.STATIC_DIR = path.join(shared.BASE_DIR, 'static')

shared.TEMPLATES_DIR = path.join(shared.EXTRAS_DIR, 'templates')

shared.FONTS_DIR = path.join(shared.TEMPLATES_DIR, 'fonts')
shared.POSTERS_DIR = path.join(shared.TEMPLATES_DIR, 'posters')
shared.BUILT_POSTERS_DIR = path.join(shared.POSTERS_DIR, 'built')

shared.PHOTOS_DIR = path.join(shared.STATIC_DIR, 'photos')

# Persistent int vars
shared.DB_CONNECT_TIMEOUT = 10  # seconds
shared.EMPLOYEE_PHOTO_HEIGHT = 280  # employee photo height (px)
shared.EMPLOYEE_PHOTO_WIDTH = 280  # employee photo width (px)
shared.FETCH_ROWS = 1000  # rows count
shared.MAX_SCHEDULER_WORKERS = 1  # workers count


shared.file_vars = ExtraFileVars()
# Load information from the *.properties file
shared.file_vars.load('properties',
                      path.join(shared.EXTRAS_DIR, 'default.properties'))

# Load information from the *.properties file
shared.file_vars.load('messenger',
                      path.join(shared.EXTRAS_DIR, 'messenger.properties'))

# Load information from the *.properties file
shared.file_vars.load('posters',
                      path.join(shared.POSTERS_DIR, 'posters.json'))


# Logger create and configuration
try:
    for claim_folder in (shared.LOGS_DIR,):
        helpers.create_folder(claim_folder)
except OSError as exc:
    sys.stderr.write(f'{exc.strerror} logs')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
try:
    logging.basicConfig(filename=path.join(shared.LOGS_DIR, f'{now().to_cookie_string()}.log'),
                        level=logging.DEBUG)
except FileNotFoundError:
    logging.basicConfig(filename=path.join(shared.BASE_DIR, f'{now().to_cookie_string()}.log'),
                        level=logging.DEBUG)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
