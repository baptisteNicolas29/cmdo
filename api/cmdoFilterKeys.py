from typing import List

from maya import cmds
from maya.api import OpenMaya as om

from ..core.abstract import nodeLib, dagLib, dgLib
from ..core import plugsLib


__all__: List[str] = [
    # Generic filters
    'isCmdoNodeFilter',
    'isDgFilter',
    'isDagFilter',
    'isPlugFilter',
    'isTypeFilter',
    'isReferencedFilter',
    'objExistsFilter',
    # Naming Filters
    'hasPrefixFilter',
    'hasSuffixFilter',
    'hasTokenFilter',
    # DAG Filters
    'isJointFilter',
    'isMeshFilter',
    'isTransformFilter',
    'isLocatorFilter',
    'isNurbsCurveFilter',
    'isNurbsSurfaceFilter',
    # DG Filters
    'isDeformerFilter',
    # Plug Filters
    'plugNotNullFilter',
]


# -------------------------------------------------------------- Generic Filters
def isCmdoNodeFilter(obj: nodeLib.Node) -> bool:
    return issubclass(obj.__class__, nodeLib.Node)


def isDgFilter(obj: nodeLib.Node) -> bool:
    return issubclass(obj.__class__, dgLib.DGNode)


def isDagFilter(obj: nodeLib.Node) -> bool:
    return issubclass(obj.__class__, dagLib.DAGNode)


def isPlugFilter(obj: om.MObject) -> bool:
    return issubclass(obj.__class__, plugsLib.Plug)


def isTypeFilter(obj: nodeLib.Node, nodeType: str) -> bool:
    return isCmdoNodeFilter(obj) and obj.isType(nodeType)


def isReferencedFilter(obj: nodeLib.Node) -> bool:
    return isCmdoNodeFilter(obj) and obj.isReferenced


def objExistsFilter(obj: nodeLib.Node) -> bool:
    return isCmdoNodeFilter(obj) and obj.exists


# --------------------------------------------------------------- Naming Filters
def hasPrefixFilter(obj: nodeLib.Node, prefix: str) -> bool:
    return obj.name.startswith(prefix)


def hasSuffixFilter(obj: nodeLib.Node, suffix: str) -> bool:
    return obj.name.endswith(suffix)


def hasTokenFilter(obj: nodeLib.Node, token: str) -> bool:
    return token in obj.name


# ------------------------------------------------------------------ DAG Filters
def isJointFilter(obj: nodeLib.Node) -> bool:
    return isDagFilter(obj) and isTypeFilter(obj, 'joint')


def isMeshFilter(obj: nodeLib.Node) -> bool:
    return isDagFilter(obj) and isTypeFilter(obj, 'mesh')


def isTransformFilter(obj: nodeLib.Node) -> bool:
    return isDagFilter(obj) and isTypeFilter(obj, 'transform')


def isLocatorFilter(obj: nodeLib.Node) -> bool:
    return isDagFilter(obj) and isTypeFilter(obj, 'locator')


def isNurbsCurveFilter(obj: nodeLib.Node) -> bool:
    return isDagFilter(obj) and isTypeFilter(obj, 'nurbsCurve')


def isNurbsSurfaceFilter(obj: nodeLib.Node) -> bool:
    return isDagFilter(obj) and isTypeFilter(obj, 'nurbsSurface')


# ------------------------------------------------------------------- DG Filters
def isDeformerFilter(obj: nodeLib.Node) -> bool:
    return isDgFilter(obj) and isTypeFilter(obj, 'geometryFilter')


# ----------------------------------------------------------------- Plug Filters
def plugNotNullFilter(plug: om.MObject) -> bool:
    return isPlugFilter(plug) and not plug.isNull

