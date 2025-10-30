from typing import List, Union, Type

from maya import cmds, mel
from maya.api import OpenMaya as om

from ..nodes.dag.meshLib import Mesh
from ..core.abstract import nodeLib, dagLib


__all__: List[str] = [
    'createCube'
]


def createCube(positions, **kwargs):
    """
    Create a new mesh cube

    :param positions:
    :param kwargs:
    :return:
    """
    return NotImplementedError('Line function not implemented yet')


def checkRemoveMeshInstances(obj: str) -> Union[str, None]:
    """
    Check the passed object makes it unique
    removes history and renames the shape

    :param obj: str, the object name to check or None if a problem occurred

    :return: Union[str, None], the name of the shape of the object
    """
    if not cmds.objExists(obj):
        cmds.warning(f'Given obj does not exist : {obj}. Aborting....')
        return None

    cmds.bakePartialHistory(obj, prePostDeformers=True)

    shapes = cmds.listRelatives(obj, c=True, s=True, f=True)
    if not shapes:
        cmds.warning(f'Given obj has no shapes : {obj}. Aborting....')
        return None

    if len(cmds.listRelatives(shapes, ap=True)) > 1:
        cmds.select(obj)
        mel.eval('ConvertInstanceToObject()')

    newShapeName = cmds.rename(
        cmds.listRelatives(obj, c=True, s=True, f=True)[0],
        f'{obj}Shape'
    )

    return newShapeName
