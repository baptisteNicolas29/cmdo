from typing import List

from maya import cmds
from maya.api import OpenMaya as om

from ..core.abstract import nodeLib, dagLib, dgLib
from ..core import plugsLib


__all__: List[str] = [
    'resetTransformMap',
    'resetPlugToDefaultMap'
]


def resetTransformMap(obj: dagLib.DAGNode) -> None:
    obj.resetTransformationMatrix()


def resetPlugToDefaultMap(plug: plugsLib.Plug) -> None:
    if plug.isNull or plug.isProxy or plug.isDestination or plug.isLocked:
        return

    defaultValue = cmds.attributeQuery(
        plug.name().split(".")[-1],
        node=plug.node().name,
        listDefault=True
    )

    plug.value = defaultValue[0] if defaultValue else 0.0

