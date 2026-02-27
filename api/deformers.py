from typing import List, Union

from maya import cmds
from maya.api import OpenMaya as om

from . import history, hierarchy, graph
from ..core.cmdoTyping import CmdoObject
from ..core.exceptions import CmdoException


__all__: List[str] = [
    'skinAs',
    'resetSkin',
    'getJointsNotInSkinHierarchy',
]


# ------------------------------------------------------------- SKINCLUSTER

# TODO: wierd things are going on when trying to use skinAs
def skinAs(source: str, destination: str, smooth: bool = False, **kwargs) -> Union[om.MObject, None]:
    """
    Bind a destination mesh based on the influence list and weights
        of the skinCluster of a source mesh.

    :param source: Source mesh that will be used to determine influence list 
        and weights of destination mesh.
    :param destination: Destination mesh to bind based on source mesh 
        skinCluster.
    :param smooth: Smooth incoming skinCluster weights for destination mesh.
    """

    # Check inputs
    if not cmds.objExists(source):
        raise CmdoException(f'Source object "{source}" does not exist!')

    if not cmds.objExists(destination):
        raise CmdoException(f'Destination object "{destination}" does not exist!')

    # Get source skinCluster
    sourceSkin = history.getDeformers(source, types="skinCluster")
    if cmds.objectType(destination) == 'mesh':
        destination = cmds.listRelatives(destination, parent=True)[0]

    if not sourceSkin:
        cmds.warning(f'Could not find skinCluster on {source = }')
        return None

    sourceSkin = sourceSkin[0]

    # Check destination skinCluster
    destinationSkin = history.getDeformers(destination, types="skinCluster")
    if destinationSkin:
        destinationSkin = destinationSkin[0]

    # Build destination skinCluster
    if not destinationSkin:
        sourceInfluences = cmds.skinCluster(sourceSkin.name, query=True, influence=True)
        destinationPrefix = destination.split(':')[-1].split('|')[-1]

        # since we include hidden selection
        # we make sure we don't skin orig shapes
        destination = [
            dest
            for dest in cmds.listRelatives(destination, shapes=True)
            if not cmds.getAttr(f'{dest}.intermediateObject')
        ][0]

        destinationSkin = cmds.skinCluster(
            sourceInfluences,
            destination,
            toSelectedBones=True,
            removeUnusedInfluence=False,
            includeHiddenSelections=True,
            name=f'{destinationPrefix}_skinCluster'
        )[0]

    # Copy skin weights
    cmds.copySkinWeights(
        sourceSkin=str(sourceSkin),
        destinationSkin=str(destinationSkin),
        surfaceAssociation=kwargs.pop('surfaceAssociation', 'closestPoint'),
        influenceAssociation=kwargs.pop('influenceAssociation', 'name'),
        noMirror=True,
        smooth=smooth,
        **kwargs
    )

    # Return result
    return graph.ls(destinationSkin)[0]


def resetSkin(nodes: List[str]) -> None:
    """
    Reset the skinClusters bindPreMatrix values with the current matrix values

    :param nodes: List[str], nodes to reset skin for

    """
    # TODO: upgrade to take om & cmdo types

    if isinstance(nodes, str):
        nodes = [nodes]

    for node in nodes:
        skinClusters = history.getDeformers(node, 'skinCluster')

        if not skinClusters:
            print(f'No skinCluster found for : {node}')
            continue

        for skinCluster in skinClusters:
            connections = cmds.listConnections(
                f"{skinCluster}.matrix",
                source=True, destination=False,
                plugs=True, connections=True
            )
            destinations = connections[0::2]
            sources = connections[1::2]

            for src, dest in zip(sources, destinations):
                mat = cmds.getAttr(f"{src.split('.')[0]}.worldInverseMatrix")
                cmds.setAttr(
                    dest.replace('matrix', 'bindPreMatrix'),
                    *mat, type='matrix'
                )


# fonction to reset from skincluster directly and not from nodes
# def resetSkin(skinClusters: List[str]) -> None:
#
#     for skinCluster in skinClusters:
#         connections = cmds.listConnections(
#             f"{skinCluster}.matrix",
#             source=True, destination=False,
#             plugs=True, connections=True
#         )
#         destinations = connections[0::2]
#         sources = connections[1::2]
#
#         for src, dest in zip(sources, destinations):
#             # print(src, dest)
#             mat = cmds.getAttr(f"{src.split('.')[0]}.worldInverseMatrix")
#             cmds.setAttr(dest.replace('matrix', 'bindPreMatrix'), *mat, type='matrix')
#
#         print(f'Finished resetting {skinCluster = }')


def getJointsNotInSkinHierarchy(objList: List[str] = None, jointWildcard: str = '*_skn') -> graph.Graph:
    """
    Get a list of joints not in any skin of given meshes

    :param objList: meshes to check whether they are in the skin hierarchy
    :param jointWildcard: wildcard string for searching joints

    :return: Graph, joints not in the skin hierarchy

    """
    skinHierarchy = set()

    def filter_func(joint):
        """
        Filter joints not in given hierarchy and not connected to a skinCluster
        """
        connection = cmds.listConnections(
            joint, source=False, destination=True, type='skinCluster'
        )
        return joint not in skinHierarchy and connection is None

    if objList is None:
        objList = cmds.ls(selection=True)

    elif not isinstance(objList, list):
        objList = [objList]

    for obj in objList:
        influences = cmds.skinCluster(obj, query=True, influence=True)

        # build skin hierarchy list
        for influence in influences:
            if influence in skinHierarchy:
                continue

            skinHierarchy.update(
                set(hierarchy.getHierarchyRoot(influence))
            )

    skeleton = cmds.ls(jointWildcard, type='joint')

    jointsNotInSkin = list(
        filter(filter_func, skeleton)
    )

    return graph.ls(jointsNotInSkin)
