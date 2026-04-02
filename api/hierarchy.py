from typing import List, Union, Type, Dict

from maya import cmds
from maya.api import OpenMaya as om

from . import graph
from ..core.abstract import nodeLib, dagLib
from ..core.cmdoTyping import CmdoObject, CmdoList


__all__: List[str] = [
    'getAllChildren',
    'getDirectChildren',
    'getRootParent',
    'getHierarchyRoot',
    'getShortestParent',
    'getDagRoots',
]


def getAllChildren(node: Union[str, Type[dagLib.DAGNode]]) -> List[str]:
    """
    Get all children of the given node

    :param node: Union[str, Type[dagLib.DAGNode]]: node to get all children from

    :return: List[str]: all children of the given node
    """

    if isinstance(node, str):
        dag = dagLib.DAGNode(node).dagPath
    else:
        dag = node.dagPath

    traversed = set()
    iterator = om.MItDag(om.MItDag.kDepthFirst)
    iterator.reset(dag)
    iterator.next()

    while not iterator.isDone():

        path = iterator.partialPathName()

        if path in traversed:
            iterator.prune()
            iterator.next()
            continue

        traversed.add(path)
        iterator.next()

    return list(traversed)


def getDirectChildren(node: str, **kwargs) -> List[str]:
    """
    Get the direct children of the given object

    :param node: the object for which to get direct children

    :return: List[str], list of direct children corresponding to the arguments
    """

    if not cmds.objExists(node):
        cmds.warning(f'Given obj does not exist : {node}. Aborting....')
        return []

    return cmds.listRelatives(node, children=True, **kwargs)


def getRootParent(node: str) -> Union[str, None]:
    """
    Get the root parent of the object

    :param node: str, a maya object to find the parent for

    :return: str, the name of the root parent
    """

    if not cmds.objExists(node):
        cmds.warning(f'Given obj does not exist : {node}. Aborting....')
        return None

    topParent = node
    while (parent := cmds.listRelatives(topParent, parent=True)) is not None:
        topParent = parent[0]

    return topParent


def getHierarchyRoot(node: str, **kwargs) -> List[str]:
    """
   Makes a list of all the hierarchy leading to the given obj

   :param node: a maya object to find the parent for
   :param kwargs: key word arguments for the listRelatives maya command

   :return: List[str], the name of all objects in the given objects hierarchy
   """

    if not cmds.objExists(node):
        cmds.warning(f'Given obj does not exist : {node}. Aborting....')
        return []

    hierarchy = [node]
    parent = node

    while (prt := cmds.listRelatives(parent, parent=True, **kwargs)) is not None:
        parent = prt[0]
        hierarchy.append(parent)

    return hierarchy


def getShortestParent(node: CmdoObject, graphList: CmdoList, asStr: bool = True) -> Union[nodeLib.Node, str, None]:
    """
    Get the first parent of specified node inside the given graph


    :param node: CmdoObject, the node to get the parent for
    :param graphList: CmdoList, the graph to search in for the parent
    :param asStr: bool, get a string of nodeLib.Node

    :return: Union[nodeLib.Node, str, None]: the parent if found
    """

    if isinstance(graphList, om.MSelectionList):
        graphList = graph.Graph().copy(graphList)

    else:
        graphList = graph.ls(graphList)

    if isinstance(node, (str, om.MObject)):
        node = graph.ls(node)[0]

    item = node
    while not item.isNull():
        for other in graphList:
            if item == other and item != node:
                return other.name if asStr else other

        item = item.parent[0]

    return None


def getDagRoots(nodes: CmdoList, safe: bool = True) -> graph.Graph:
    """
    Get the dag nodes roots from a set of given nodes

    :param nodes: CmdoList, node list to process
    :param safe: bool, if safe function will not fail (bypass the not dagNodes) else bypass the dgNodes

    :return: Graph: graph which contains the dagRootNodes or empty graph
    """

    if isinstance(nodes, list) or isinstance(nodes, om.MSelectionList):
        nodes = graph.ls(nodes)

    previous = graph.Graph()
    roots = graph.Graph()

    for item in nodes:
        itemObj = item if isinstance(item, nodeLib.Node) else item
        previous.add(itemObj)

        if (not safe) and itemObj.isDagNode:
            raise TypeError(f'{itemObj} is not a dagNode')

        if safe and itemObj.isDagNode:
            continue

        isChild = False
        mfnDagNode = itemObj.mfnDagNode
        for other in nodes - previous:
            isChild |= mfnDagNode.isChildOf(other)

        if not isChild:
            roots.add(itemObj)

    return roots
