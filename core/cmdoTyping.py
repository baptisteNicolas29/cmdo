"""
Module describing some of the most used types in cmdo to make it easier for
type hinting

"""

from typing import Union, List, Type, Tuple

from maya.api import OpenMaya as om


__all__: List[str] = [
    'CmdoObject',
    'CmdoList',
    'CmdoNumber'
]


CmdoObject = Type[Union[str, om.MObject]]

CmdoNumber = Type[Union[int, float]]

CmdoList = Type[Union[List, Tuple, om.MSelectionList]]
