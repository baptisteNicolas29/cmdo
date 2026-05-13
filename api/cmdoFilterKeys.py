from typing import List

from maya import cmds
from maya.api import OpenMaya as om

from ..core.abstract import nodeLib, dagLib, dgLib
from ..core import plugsLib


__all__: List[str] = [
    'isTypeFilter',
    'isDagFilter',
    'isPlugFilter',
    'isReferencedFilter',
    'isJointFilter',
    'isMeshFilter',
    'isTransformFilter',
    'isLocatorFilter',
    'isDeformerFilter',
]


# Generic Filters
def isTypeFilter(obj: nodeLib.Node, nodeType: str) -> bool: return obj.isType(nodeType)
def isDgFilter(obj: nodeLib.Node) -> bool: return issubclass(obj.__class__, dgLib.DGNode)
def isDagFilter(obj: nodeLib.Node) -> bool: return issubclass(obj.__class__, dagLib.DAGNode)
def isPlugFilter(obj: om.MObject) -> bool: return issubclass(obj.__class__, plugsLib.Plug)
def isReferencedFilter(obj: nodeLib.Node) -> bool: return issubclass(obj.__class__, nodeLib.Node) and obj.isReferenced


# Naming Filters
def hasPrefixFilter(obj: nodeLib.Node, prefix: str) -> bool: return obj.name.startswith(prefix)
def hasSuffixFilter(obj: nodeLib.Node, suffix: str) -> bool: return obj.name.endswith(suffix)
def hasTokenFilter(obj: nodeLib.Node, token: str) -> bool: return token in obj.name


# DAG Filters
def isJointFilter(obj: nodeLib.Node) -> bool: return isDagFilter(obj) and isTypeFilter(obj, 'joint')
def isMeshFilter(obj: nodeLib.Node) -> bool: return isDagFilter(obj) and isTypeFilter(obj, 'mesh')
def isTransformFilter(obj: nodeLib.Node) -> bool: return isDagFilter(obj) and isTypeFilter(obj, 'transform')
def isLocatorFilter(obj: nodeLib.Node) -> bool: return isDagFilter(obj) and isTypeFilter(obj, 'locator')


# DG Filters
def isDeformerFilter(obj: nodeLib.Node) -> bool: return isDgFilter(obj) and isTypeFilter(obj, 'geometryFilter')


# Plug Filters

