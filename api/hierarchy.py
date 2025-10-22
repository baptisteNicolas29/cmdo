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

    Args:
        node: Union[str, Type[dagLib.DAGNode]]:
            Le noeud à partir duquel on veut récupérer les enfants.

    Returns:
        List[str]:
            La liste de tous les enfants des noeuds.
    """

    if isinstance(node, str):
        sel = om.MSelectionList()
        sel.clear()
        sel.add(node)
        dag = sel.getDagPath(0)
    else:
        dag = node.maya_dagPath

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
    Args:
        node: the object for which to get direct children
        **kwargs: keyword arguments for the listRelative maya command
    Returns:
        a list of direct children corresponding to the given arguments
    """

    if not cmds.objExists(node):
        cmds.warning(f'Given obj does not exist : {node}. Aborting....')
        return []

    return cmds.listRelatives(node, children=True, **kwargs)


def getRootParent(node: str) -> Union[str, None]:
    """
    Get the root parent of the object
    Args:
        node: a maya object to find the parent for

    Returns:
        the name of the root parent
    """
    if not cmds.objExists(node):
        cmds.warning(f'Given obj does not exist : {node}. Aborting....')
        return None

    top_parent = node
    while (parent := cmds.listRelatives(top_parent, parent=True)) is not None:
        top_parent = parent[0]

    return top_parent


def getHierarchyRoot(node: str, **kwargs) -> List[str]:
    """
       Makes a list of all the hierarchy leading to the given obj
       Args:
           node: a maya object to find the parent for
           kwargs: key word arguments for the listRelatives maya command
       Returns:
           the name of all objects in the given objects hierarchy
       """

    if not cmds.objExists(node):
        cmds.warning(f'Given obj does not exist : {node}. Aborting....')
        return []

    joint_hierarchy = [node]
    parent = node

    while (prt := cmds.listRelatives(parent, parent=True, **kwargs)) is not None:
        parent = prt[0]
        joint_hierarchy.append(parent)

    return joint_hierarchy


def getShortestParent(node: CmdoObject, graphList: CmdoList, asStr: bool = True) -> Union[nodeLib.Node, str, None]:
    """
    Get the first parent of specified node inside the given graph

    Args:
        node: CmdoObject, the node to get the parent for
        graphList: CmdoList, the graph to search in for the parent
        asStr: bool, get a string of nodeLib.Node

    Returns:
        Union[nodeLib.Node, str, None]: the parent if found
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

    Args:
        nodes: CmdoList, node list to process
        safe: bool, if safe function will not fail (bypass the not dagNodes) else bypass the dgNodes

    Returns:
        Graph: void one if source graph has no DagNode else return graph who contain the dagRootNodes
    """

    if isinstance(nodes, list) or isinstance(nodes, om.MSelectionList):
        nodes = graph.ls(nodes)

    previous = graph.emptyGraph()
    roots = graph.emptyGraph()

    for item in nodes:
        item_obj = item if isinstance(item, nodeLib.Node) else item
        previous.add(item_obj)

        if (not safe) and item_obj.isDagNode:
            raise TypeError(f'{item_obj} is not a dagNode')

        if safe and item_obj.isDagNode:
            continue

        is_child = False
        mfnDagNode = item_obj.mfnDagNode
        for other in nodes - previous:
            is_child |= mfnDagNode.isChildOf(other)

        if not is_child:
            roots.add(item_obj)

    return roots
