from typing import List, Union, Type

import maya.cmds as mc
import maya.api.OpenMaya as om

from . import graph
from ..nodes.dag.curveLib import Curve
from ..core.abstract import nodeLib, dagLib
from ..core.exceptions import CmdoException
from ..core.cmdoTyping import CmdoNumber


__all__: List[str] = [
    'createCircle',
    'createBox',
    'createCross'
]


# TODO: Move to more task oriented library (aka: rigging)
def createCircle(name='nurbsCircle', radius: CmdoNumber = 1.0, **kwargs):
    """
    Create a basic circle

    :param name: str, the name of the node to create
    :param radius: float, change the default size of the circle
    :return:
        Curve: the created object
    """

    transform, make_nurbs = mc.circle(name=name, radius=radius, **kwargs)

    graph.delete(make_nurbs)

    return graph.ls(transform)[0]


def createBox(name='nurbsBox', size: Union[CmdoNumber, List[CmdoNumber]] = 1.0, **kwargs):
    """
    Create a basic Box

    :param name: str, the name of the node to create
    :param size: float, change the default size of the box

    :return:
        Curve: the created object
    """
    if isinstance(size, (int, float)) or len(size) == 1:
        sizeX = sizeY = sizeZ = size

    elif len(size) == 3:
        sizeX, sizeY, sizeZ = size

    else:
        raise CmdoException(
            f'[cmdo.api.curves.createBox]: size argument must be length 1 or 3,'
            f' got: {len(size)} - {size}'
        )

    curve_data = {
        "degree": 1,
        "form": 1,
        "is2D": False,
        "rational": True,
        "knots": [
            0.0, 1.0, 2.0, 3.0, 4.0, 5.0,
            6.0, 7.0, 8.0, 9.0, 10.0, 11.0,
            12.0, 13.0, 14.0, 15.0, 16.0
        ],
        "cvs": [
            [-sizeX, sizeY, sizeZ, 1.0],
            [-sizeX, -sizeY, sizeZ, 1.0],
            [sizeX, -sizeY, sizeZ, 1.0],
            [sizeX, sizeY, sizeZ, 1.0],
            [-sizeX, sizeY, sizeZ, 1.0],
            [-sizeX, sizeY, -sizeZ, 1.0],
            [-sizeX, -sizeY, -sizeZ, 1.0],
            [-sizeX, -sizeY, sizeZ, 1.0],
            [sizeX, -sizeY, sizeZ, 1.0],
            [sizeX, -sizeY, -sizeZ, 1.0],
            [sizeX, sizeY, -sizeZ, 1.0],
            [sizeX, sizeY, sizeZ, 1.0],
            [-sizeX, sizeY, sizeZ, 1.0],
            [-sizeX, sizeY, -sizeZ, 1.0],
            [sizeX, sizeY, -sizeZ, 1.0],
            [sizeX, -sizeY, -sizeZ, 1.0],
            [-sizeX, -sizeY, -sizeZ, 1.0]
        ]
    }

    parent = (
            graph.ls(kwargs.get('parent'), '')
            or [om.MObject.kNullObj]
    )[0]

    mfnCurve = om.MFnNurbsCurve()
    mfnCurve.create(
        curve_data.get('cvs'),
        curve_data.get('knots'),
        curve_data.get('degree'),
        curve_data.get('form'),
        curve_data.get('is2D'),
        curve_data.get('rational'),
        parent=parent
    )
    # mfnCurve.setName(name)

    curveParent = graph.ls(mfnCurve.parent(0))[0]
    curveParent.name = name

    return curveParent


def createCross(name='nurbsCross', size: CmdoNumber = 1.0, **kwargs):

    """
    Create a basic Cross

    :param name: str, the name of the node to create
    :param size: float, change the default size of the cross
    :return:
        Curve: the created object
    """

    curve_data = {
        "degree": 1,
        "form": 1,
        "is2D": False,
        "rational": True,
        "knots": [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0],
        "cvs": [
            [0.0, size, 0.0, 1.0], [0.0, -size, 0.0, 1.0], [0.0, 0.0, 0.0, 1.0],
            [0.0, 0.0, -size, 1.0], [0.0, 0.0, size, 1.0], [0.0, 0.0, 0.0, 1.0],
            [size, 0.0, 0.0, 1.0], [-size, 0.0, 0.0, 1.0]
        ]
    }

    parent = (
            graph.ls(kwargs.get('parent'), '')
            or [om.MObject.kNullObj]
    )[0]

    mfnCurve = om.MFnNurbsCurve()
    mfnCurve.create(
        curve_data.get('cvs'),
        curve_data.get('knots'),
        curve_data.get('degree'),
        curve_data.get('form'),
        curve_data.get('is2D'),
        curve_data.get('rational'),
        parent=parent
    )

    curveParent = graph.ls(mfnCurve.parent(0))[0]
    curveParent.name = name

    return curveParent
