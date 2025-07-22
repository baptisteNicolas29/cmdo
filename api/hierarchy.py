from typing import List, Union, Type, Dict

import maya.cmds as mc
import maya.api.OpenMaya as om

from ..core import graph_lib
from ..core.abstract import node_lib, dag_lib


__all__ = [
    'getAllChildren',
    'getDirectChildren',
    'getRootParent',
    'getHierarchyRoot',
    'getShortestParent',
    'getDagRoots',
]


def getAllChildren(node: Union[str, Type[dag_lib.DAGNode]]) -> List[str]:

    """
    Get all children of the given node

    Args:
        node: Union[str, Type[dag_lib.DAGNode]]:
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

    if not mc.objExists(node):
        mc.warning(f'Given obj does not exist : {node}. Aborting....')
        return []

    return mc.listRelatives(node, children=True, **kwargs)


def getRootParent(node: str) -> Union[str, None]:
    """
    Get the root parent of the object
    Args:
        node: a maya object to find the parent for

    Returns:
        the name of the root parent
    """
    if not mc.objExists(node):
        mc.warning(f'Given obj does not exist : {node}. Aborting....')
        return None

    top_parent = node
    while (parent := mc.listRelatives(top_parent, p=True)) is not None:
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

    if not mc.objExists(node):
        mc.warning(f'Given obj does not exist : {node}. Aborting....')
        return []

    joint_hierarchy = [node]
    parent = node

    while (prt := mc.listRelatives(parent, p=True, **kwargs)) is not None:
        parent = prt[0]
        joint_hierarchy.append(parent)

    return joint_hierarchy


def getShortestParent(
    node: Union[str, om.MObject, node_lib.Node],
    graph: Union[List[str], List[node_lib.Node], om.MSelectionList],
    as_str: bool = True,
) -> Union[node_lib.Node, str, None]:
    """
    return the first parent of specified node inside the given graph

    Args:
        node (Union[str, Node, MObject]):
            le node d'on on cherche le parent

        graph (Union[List[str], List[Node], MSelectionList]):
            le graph ou on cherche le parent theorique

        as_str (bool):
            Vrais pour retourner une chaine de caractere Faut pour retourner un Node object

    Returns:
        str si asStr et vrais sinon Node
    """

    if isinstance(graph, om.MSelectionList):
        graph = graph_lib.Graph().copy(graph)

    else:
        # just clear the inputs data
        graph = graph_lib.Graph.ls(graph)

    if isinstance(node, (str, om.MObject)):
        node = node_lib.Node(node)

    item = node
    while not item.maya_object.isNull():
        for other in graph:
            if item.maya_object == other.maya_object:
                if item.maya_object != node.maya_object:
                    return other.name if as_str else other

        item = item.parent[0]

    return None


def getDagRoots(
    nodes: Union[List[str], List[node_lib.Node], om.MSelectionList],
    safe: bool = True,
) -> graph_lib.Graph:
    """
    get the dag nodes roots from a set of given nodes

    Args:
        nodes: Union[[List[str], List[Node], om.MSelectionList]]:
            node list you want to process

        safe: (bool):
            if safe function will not fail (bypass the not dagNodes) else bypass the dgNodes

    Returns:
        Graph: void one if source graph has no DagNode else return graph who contain the dagRootNodes
    """

    if isinstance(nodes, list):
        tmp = graph_lib.Graph()

        for node in nodes:
            tmp.add(node)

        nodes = tmp

    elif isinstance(nodes, om.MSelectionList):
        nodes = graph_lib.Graph(nodes)

    previous = graph_lib.Graph()
    roots = graph_lib.Graph()
    for item in nodes:
        item_obj = item.maya_object if isinstance(item, node_lib.Node) else item
        previous.add(item_obj)

        if (not safe) and (not item_obj.hasFn(om.MFn.MFnDagNode)):
            raise TypeError(f'{node} is not a dagNode')

        if safe and (not item_obj.hasFn(om.MFn.kDagNode)):
            continue

        is_child = False
        mfnDagNode = om.MFnDagNode(item_obj)
        for other in nodes - previous:
            is_child |= mfnDagNode.isChildOf(other.maya_object)

        if not is_child:
            roots.add(item_obj)

    return roots
