"""
Module describing some of the most used types in cmdo to make it easier for
type hinting

"""

from typing import Union, List, Type, Tuple

from maya.api import OpenMaya as om


__all__: List[str] = [
    'CmdoObject',
    'CmdoPlug',
    'CmdoList',
    'CmdoNumber'
]


CmdoObject = Type[Union[str, om.MObject]]

CmdoPlug = Type[Union[str | om.MPlug]]

CmdoNumber = Type[Union[int, float]]

CmdoList = Type[Union[List, Tuple, om.MSelectionList]]
