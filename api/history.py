from typing import List, Union

from maya import cmds
from maya.api import OpenMaya as om

from . import graph


__all__: List[str] = [
    'getDeformers',
    'getNodeHistoryByType',
]


def getDeformers(node: Union[str, om.MObject], types: Union[str, List[str]]) -> graph.Graph:
    """
    Get deformers from node history

    Args:
        node: Union[str, om.MObject], node to get deformers for
        types: Union[str, List[str]], types of deformers to search for

    Returns:
        graph.Graph: a list of found deformers
    """

    if not isinstance(types, list):
        types = [types]

    history = graph.listHistory(node)
    deformers = list(filter(
        lambda d: d.type in types,
        history
    ))

    return graph.ls(*deformers)


def getNodeHistoryByType(node: str, **kwargs) -> List[str]:
    """

    Args:
        node: the node to start the search from
        kwargs: all the keyword arguments to pass to the ls return command

    Returns:
        a list of nodes corresponding to the demand
    """

    past_history = set(cmds.listHistory(
        node, allConnections=True, fastIteration=True
    ))
    future_history = set(cmds.listHistory(
        node, future=True, allConnections=True, fastIteration=True
    ))

    past_history.update(future_history)

    return cmds.ls(*list(past_history), **kwargs)


# def get_deformers(target: str, deformer_type: list | str = None) -> list | None:
#     """
#     Only works for maya 2018 and up
#     Queries the deformer(s) applied to a target node
#     Accepted deformer types are :
#         [normal] : [
#             'skinCluster', 'blendShape', 'nonLinear', 'ffd', 'cluster',
#             'tension', 'deltaMush', 'wrap', 'tweak', 'wire', 'shrinkWrap',
#             'softMod', 'sculpt'
#         ]
#         [nonLinear] : [
#             'bend', 'flare', 'sine', 'squash', 'twist', 'wave'
#         ]
#     :param target: the node name to query deformers from
#     :param deformer_type: the deformer type to search for
#     :return: a list of deformers or None
#     """
#
#     deformer_list = cmds.findDeformers(target)
#     if not deformer_list:
#         return None
#
#     if deformer_type is None:
#         return deformer_list
#
#     wanted_deformer = [
#         x for x in deformer_list
#         if cmds.nodeType(x) in deformer_type
#     ]
#
#     if wanted_deformer:
#         return wanted_deformer
#
#     for deform in deformer_list:
#
#         if cmds.objExists(f'{deform}.deformerData'):
#             deformer_handle = cmds.listConnections(
#                 f'{deform}.deformerData', s=True, sh=True
#             )[0]
#
#             if deformer_type.capitalize() in cmds.nodeType(deformer_handle):
#                 wanted_deformer.append(deformer_handle)
#
#     return wanted_deformer or None
