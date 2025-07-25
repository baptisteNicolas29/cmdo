from typing import Union, List, Type, Tuple, Set


from maya.api import OpenMaya as om, OpenMayaAnim as oma

__all__ = [
    'CmdoObject',
    'CmdoList',
    'CmdoNumber'
]


CmdoObject = Type[Union[str, om.MObject]]

CmdoNumber = Type[Union[int, float]]

CmdoList = Type[Union[List, Tuple, om.MSelectionList]]
