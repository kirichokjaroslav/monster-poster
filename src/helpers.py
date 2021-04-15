from __future__ import annotations, generators

import base64
import errno
import functools as ft
import json
from inspect import currentframe
from io import BytesIO
from mimetypes import guess_extension, guess_type
from os import makedirs, path, remove
from typing import (
    Any,
    AnyStr,
    Callable,
    Dict,
    FrozenSet,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    cast,
)

from PIL import Image
from returns.result import safe


"""
    @author: Jaroslav Kirichok
    @authors: Delete this text-line if you work with the code below
              and write your name
    @license: GNU GENERAL PUBLIC LICENSE 3
"""


__all__: \
    Sequence[str] = ('create_folder',
                     'disallow',
                     'from_request',
                     'prepare_poster',
                     'remove_file',
                     'require_fields',
                     'time_interpretation',
                     'upload_file',
                     'upload_ib64')

# Types definitions
ReturnType = TypeVar('ReturnType')


def create_folder(folder_path: str) -> None:
    """Function for creating a folder in a given path.

    Args:
        folder_path: Folder path to create

    Raises:
        RuntimeError: If failed to create folder.
    """
    try:
        makedirs(folder_path, exist_ok=True)
    except TypeError:
        try:
            makedirs(folder_path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and path.isdir(folder_path):
                return None
            else:
                raise OSError('An error occurred while creating the folder for.')


def disallow(func: Callable[..., ReturnType]) -> Callable[..., ReturnType]:
    """A simple decorator that creates a 'private' method (as C++, or
    Java access modifier) and denies calling it from outside.

    Args:
        func: Function to decorate

    Returns:
        A wrapper function that decorates.
    """
    class_name: \
        Optional[str] = currentframe().f_back.f_code.co_name  # type: ignore

    @ft.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> ReturnType:
        call_frame = currentframe().f_back  # type: ignore
        # Only methods of same class should be able to call private
        # methods of the class, and no one else
        if 'self' in call_frame.f_locals:
            caller_class_name = call_frame.f_locals['self'].__class__.__name__
            if caller_class_name == class_name:
                return func(*args, **kwargs)
        raise RuntimeError(f'Calling a function {func.__name__} is disallow.')

    return wrapper

@safe
def from_request(request_fields: AnyStr) -> Dict[str, Any]:
    """Takes the request body as an argument and converts to the
    dictionary via json.loads().

    Args:
        request_fields: Request body from the handler

    Returns:
        Dictionary, with request body fields or None.
    """
    return cast(Dict[str, Any], json.loads(request_fields))


@safe
def remove_file(file_path: str) -> None:
    """Function safety remove file.

    Args:
        file_path: The path to the file to be deleted
    """
    remove(file_path)


def require_fields(
    request_fields: Dict[str, Any], pattern_fields: FrozenSet[str]
) -> bool:
    """Checks income request for missing and/or empty fields.

    Args:
        request_fields: Request body from handler
        pattern_fields: Set of required fields

    Returns:
        True/False, do the transmitted fields match the required fields.
    """
    if not pattern_fields.issubset(set(request_fields.keys())):
        return False
    present_fields = \
        pattern_fields.intersection(frozenset(request_fields.keys()))
    values_fields = \
        frozenset([request_fields[field] for field in present_fields])
    return False if len({'', None}.intersection(values_fields)) > 0 else True


def time_interpreter(year: int) -> str:
    """The function searches for a suitable suffix for a certain
    number of years.

    Args:
        year: Count of years to be interpreted

    Returns:
        Suitable suffix for a certain number of years.
    """
    count: \
        Dict[str, str] = {'1': 'год', '234': 'года', '567890': 'лет'}
    suffix = next(value for key, value in count.items() if str(year % 10) in key)
    # ... and return year suffix interpretation
    return 'лет' if year > 10 and str(year).startswith('1') else suffix


@safe
def upload_file(file_name: str, text: AnyStr) -> None:
    """Upload file transferred from front end.

    Args:
        file_name: Named file for write
        text: File body, got from ``request.files`` or any other place
    """
    with open(file_name, mode='wb') as fl:
        fl.write(text)


@safe
def upload_ib64(
    file_name: str, text: AnyStr, offset: Tuple[int, int] = (0, 0)
) -> str:
    """Upload image transferred from front end.

    Args:
        file_name: Named file for write
        text: BASE64 file body, got from request data or any other place

    Returns:
        If all good, - return full file name.
    """
    # Split header and body to different entities
    ib64_header, ib64_separator, ib64_body = text.partition(',')
    type, *_ = guess_type(f'{ib64_header}{ib64_separator}')
    file_ext = guess_extension(type)
    # Construct full file name
    file_name_full = f'{file_name}{file_ext}'
    # Save file
    with Image.open(BytesIO(base64.b64decode(ib64_body.strip()))) as fl:
        if ft.reduce(lambda width, height: width * height, offset) != 0:
            fl.thumbnail(offset, resample=Image.LANCZOS)
        # Save image
        fl.save(file_name_full, quality=100, optimize=True)
    # ... and return full file name
    return file_name_full
