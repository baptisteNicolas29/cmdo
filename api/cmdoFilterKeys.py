from typing import List

from ..core.abstract import nodeLib, dagLib, dgLib
from ..core import plugsLib
from .. import cmds, om


__all__: List[str] = [
    'isTypeFilter',
    'isDagFilter',
    'isPlugFilter',
    'isReferencedFilter',
    'isJointFilter',
    'isMeshFilter',
    'isTransformFilter',
    'isLocatorFilter',
]


# Generic Filters
def isTypeFilter(obj: nodeLib.Node, nodeType: str) -> bool: return obj.isType(nodeType)
def isDagFilter(obj: nodeLib.Node) -> bool: return issubclass(obj.__class__, dagLib.DAGNode)
def isPlugFilter(obj: om.MObject) -> bool: return issubclass(obj.__class__, plugsLib.Plug)
def isReferencedFilter(obj: nodeLib.Node) -> bool: return obj.isReferenced


# DAG Filters
def isJointFilter(obj: nodeLib.Node) -> bool: return isDagFilter(obj) and isTypeFilter(obj, 'joint')
def isMeshFilter(obj: nodeLib.Node) -> bool: return isDagFilter(obj) and isTypeFilter(obj, 'mesh')
def isTransformFilter(obj: nodeLib.Node) -> bool: return isDagFilter(obj) and isTypeFilter(obj, 'transform')
def isLocatorFilter(obj: nodeLib.Node) -> bool: return isDagFilter(obj) and isTypeFilter(obj, 'locator')


# DG Filters


# Plug Filters

