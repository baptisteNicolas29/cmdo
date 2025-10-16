from typing import List

from maya import cmds as mc
from maya.api import OpenMaya as om

from ..core.graphLib import Graph


__all__: List[str] = [
    'ls',
    'listRelatives',
    'listHistory',
    'listConnections',
    'createNode',
    'delete',
    'emptyGraph',
    'select',
    'duplicate'
]


def emptyGraph() -> Graph:
    """
    Get an empty Graph (maya.api.OpenMaya.MSelectionList subclass)

    Returns:
        Graph: and empty graph (list)
    """
    return Graph()


def ls(*args, **kwargs) -> Graph:
    """
    Get a list of cmdo objects depending on args, kwargs
    Imitate the maya.cmds.ls command but using OpenMaya

    Returns:
        Graph: a list of cmdo objects
    """

    return Graph.ls(*args, **kwargs)


def listHistory(*args, **kwargs) -> Graph:
    """
    Get a list of cmdo objects from the input node history
     depending on args, kwargs
    Imitate the maya.cmds.listHistory

    Returns:
        Graph: a list of cmdo objects
    """
    return Graph.listHistory(*args, **kwargs)


def listRelatives(*args, **kwargs) -> Graph:
    """
    Get a list of cmdo objects from input node hierarchy
     depending on args, kwargs

    Imitate the maya.cmds.listRelatives command

    Returns:
        Graph: a list of cmdo objects
    """
    return Graph.listRelatives(*args, **kwargs)


def listConnections(*args, **kwargs) -> Graph:
    """
    Get a list of cmdo plugs from input plugs
     depending on args, kwargs

    Imitate the maya.cmds.listConnections command

    Returns:
        Graph: a list of cmdo plugs
    """
    return Graph.listConnections(*args, **kwargs)


def createNode(nodeType: str, name: str = None, parent: om.MObject = None, **kwargs) -> om.MObject:
    """
    Create a maya node and wraps it in cmdo object class depending on node type
    Imitate the maya.cmds.createNode command

    Args:
        nodeType: str, the type of node to create
        name: str, the name of the node to create
        parent: om.MObject, the node to parent the created node to

    Returns:
        om.MObject: a maya node wrapped in cmdo object class
    """
    return Graph().createNode(nodeType, name=name, parent=parent, **kwargs)


def delete(*args, **kwargs) -> None:
    """
    Delete nodes
    Imitate the maya.cmds.delete command
    """

    Graph.delete(*args, **kwargs)


def select(*args, **kwargs) -> None:
    """
    Select nodes
    Imitate the maya.cmds.select command
    """

    Graph.select(*args, **kwargs)


def duplicate(*args, **kwargs) -> Graph:
    """
    Duplicate nodes
    Imitate the maya.cmds.duplicate command

    Returns:
        Graph: a list of duplicated objects
    """

    return Graph.duplicate(*args, **kwargs)
