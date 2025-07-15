from typing import List, Union, Type

import maya.cmds as mc
import maya.api.OpenMaya as om

from . import graph
from ..nodes.dag.curve_lib import Curve
from ..core.abstract import node_lib, dag_lib


__all__ = [
    'createCircle',
    'createLine'
]


def createCircle(name='nurbsCircle1', radius: float = 1.0, **kwargs):
    """
    Create a basic circle

    :param name: str, the name of the node to create
    :param radius: float, change the default size of the circle
    :return:
        Curve: the created object
    """

    transform, make_nurbs = mc.circle(name=name, radius=radius, **kwargs)

    mc.delete(make_nurbs)

    return graph.ls(transform)[0]


def createLine(positions, **kwargs):
    return NotImplementedError('Line function not implemented yet')
