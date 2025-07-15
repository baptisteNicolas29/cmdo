from typing import List, Union, Type

import maya.cmds as mc
import maya.api.OpenMaya as om

from ..nodes.dag.mesh_lib import Mesh
from ..core.abstract import node_lib, dag_lib


__all__ = [
    'createCube'
]


def createCube(positions, **kwargs):
    return NotImplementedError('Line function not implemented yet')
