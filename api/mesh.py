from typing import List, Union, Type

import maya.cmds as mc
import maya.api.OpenMaya as om

from ..nodes.dag.meshLib import Mesh
from ..core.abstract import nodeLib, dagLib


__all__ = [
    'createCube'
]


def createCube(positions, **kwargs):
    return NotImplementedError('Line function not implemented yet')
