from typing import List, Union

from maya import cmds
from maya.api import OpenMaya as om

from . import graph
from ..core.cmdoTyping import CmdoObject


__all__: List[str] = [
    'getDeformers',
    'getNodeHistoryByType',
]


def getDeformers(node: CmdoObject, types: Union[str, List[str]]) -> graph.Graph:
    """
    Get deformers from node history

    :param node: CmdoObject, node to get deformers for
    :param types: Union[str, List[str]], types of deformers to search for

    :return: graph.Graph: a list of found deformers
    """

    if not isinstance(types, list):
        types = [types]

    history = graph.listHistory(node)
    deformers = list(filter(
        lambda d: d.type in types,
        history
    ))

    return graph.ls(*deformers) if deformers else graph.Graph()


def getNodeHistoryByType(node: str, **kwargs) -> List[str]:
    """
    Get nodes in given node's history by type

    :param node: str, the node to start the search from
    :param kwargs: all the keyword arguments to pass to the ls return command

    :return: List[str], a list of nodes corresponding to the demand
    """

    pastHistory = set(cmds.listHistory(
        node, allConnections=True, fastIteration=True
    ))
    futureHistory = set(cmds.listHistory(
        node, future=True, allConnections=True, fastIteration=True
    ))

    pastHistory.update(futureHistory)

    return cmds.ls(*list(pastHistory), **kwargs)
