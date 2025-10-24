"""
Module to define cmdo specific exceptions

"""

from typing import List

__all__: List[str] = [
    'CmdoException',
    'CmdoPlugException'
]


class CmdoException(Exception):
    pass


class CmdoPlugException(Exception):
    pass


