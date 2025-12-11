from typing import List, Union

from maya import cmds
from maya.api import OpenMaya as om

from ..core.graphLib import Graph
from ..nodes.dag.containerLib import Container
from ..core.cmdoTyping import CmdoList


__all__: List[str] = [
    'Graph',
    'ls',
    'listRelatives',
    'listHistory',
    'listConnections',
    'createNode',
    # 'delete',
    'emptyGraph',
    # 'select',
    'duplicate',
    'duplicateWithInternalConnections',
]


def emptyGraph() -> Graph:
    """
    Get an empty Graph (maya.api.OpenMaya.MSelectionList subclass)

    :return: Graph: and empty graph (list)
    """
    return Graph()


def ls(*args, **kwargs) -> Graph:
    """
    Get a list of cmdo objects depending on args, kwargs

    Imitate the maya.cmds.ls command but using OpenMaya

    :return: Graph: a list of cmdo objects
    """

    return Graph.ls(*args, **kwargs)


def listHistory(*args, **kwargs) -> Graph:
    """
    Get a list of cmdo objects from the input node history
    depending on args, kwargs

    Imitate the maya.cmds.listHistory

    :return: Graph: a list of cmdo objects
    """

    return Graph.listHistory(*args, **kwargs)


def listRelatives(*args, **kwargs) -> Graph:
    """
    Get a list of cmdo objects from input node hierarchy
    depending on args, kwargs

    Imitate the maya.cmds.listRelatives command

    :return: Graph: a list of cmdo objects
    """

    return Graph.listRelatives(*args, **kwargs)


def listConnections(*args, **kwargs) -> Graph:
    """
    Get a list of cmdo plugs from input plugs
    depending on args, kwargs

    Imitate the maya.cmds.listConnections command

    :return: Graph: a list of cmdo plugs
    """

    return Graph.listConnections(*args, **kwargs)


def createNode(nodeType: str, name: str = None, parent: om.MObject = None, **kwargs) -> om.MObject:
    """
    Create a maya node and wraps it in cmdo object class depending on node type

    Imitate the maya.cmds.createNode command

    :param nodeType: str, the type of node to create
    :param name: str, the name of the node to create
    :param parent: om.MObject, the node to parent the created node to

    :return: om.MObject: a maya node wrapped in cmdo object class
    """

    return Graph().createNode(nodeType, name=name, parent=parent, **kwargs)


# def delete(*args, **kwargs) -> None:
#     """
#     Delete nodes
#     Imitate the maya.cmds.delete command
#     """
#
#     Graph.delete(*args, **kwargs)


# def select(*args, **kwargs) -> None:
#     """
#     Select nodes
#
#     Imitate the maya.cmds.select command
#     """
#
#     Graph.select(*args, **kwargs)


def duplicate(*args, **kwargs) -> Graph:
    """
    Duplicate nodes

    Imitate the maya.cmds.duplicate command

    :return: Graph: a list of duplicated objects
    """

    return Graph.duplicate(*args, **kwargs)


def duplicateWithInternalConnections(graph: CmdoList, inputConnections: bool = False) -> Union[Graph, None]:
    """
    This function duplicate given nodes, keeps connections and set attributes

    :param graph: List[str], node compose the graph to be duplicated
    :param inputConnections: bool, allow the graph to keep input connections

    :return: List[str] of the new nodes created
    """

    if len(graph) == 0:
        return None

    sourceContainer = Container.containerize(Graph.ls(graph))
    duplicatedContainer = Container(
            cmds.duplicate(
                str(sourceContainer),
                inputConnections=inputConnections
            )[0]
        )

    toLock = sourceContainer.nodes + duplicatedContainer.nodes
    toReturn = duplicatedContainer.nodes

    cmds.lockNode(toLock, lock=True)
    cmds.container(str(sourceContainer), removeContainer=True, edit=True)
    cmds.container(str(duplicatedContainer), removeContainer=True, edit=True)
    cmds.lockNode(toLock, lock=False)

    return toReturn
