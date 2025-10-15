from typing import List, Union

from maya import cmds as mc
from maya.api import OpenMaya as om

from . import history, hierarchy, graph


__all__ = [
    'skinAs',
    'resetSkin',
    'getJointsNotInSkinHierarchy',
]


# ------------------------------------------------------------- SKINCLUSTER

# TODO: wierd things are going on when trying to use skinAs
def skinAs(source: str, destination: str, smooth: bool = False, **kwargs) -> Union[om.MObject, None]:
    """
    Bind a destination mesh based on the influence list and weights of the 
    skinCluster of a source mesh.

    :param source: Source mesh that will be used to determine influence list 
    and weights of destination mesh.
    :param destination: Destination mesh to bind based on source mesh 
    skinCluster.
    :param smooth: Smooth incoming skinCluster weights for destination mesh.
    """

    # Check inputs
    if not mc.objExists(source):
        raise Exception(f'Source object "{source}" does not exist!')

    if not mc.objExists(destination):
        raise Exception(f'Destination object "{destination}" does not exist!')

    # Get source skinCluster
    source_skin = history.getDeformers(source, types="skinCluster")

    if mc.objectType(destination) == 'mesh':
        destination = mc.listRelatives(destination, parent=True)[0]

    if not source_skin:
        mc.warning(f'Could not find skinCluster on {source = }')
        return None

    source_skin = source_skin[0]

    # Check destination skinCluster
    destination_skin = history.getDeformers(destination, types="skinCluster")
    if destination_skin:
        destination_skin = destination_skin[0]

    # Build destination skinCluster
    if not destination_skin:
        source_influences = mc.skinCluster(source_skin, query=True, influence=True)
        destination_prefix = destination.split(':')[-1].split('|')[-1]

        # since we include hidden selection
        # we make sure we don't skin orig shapes
        destination = [
            dest
            for dest in mc.listRelatives(destination, shapes=True)
            if not mc.getAttr(f'{dest}.intermediateObject')
        ][0]

        destination_skin = mc.skinCluster(
            source_influences,
            destination,
            toSelectedBones=True,
            removeUnusedInfluence=False,
            includeHiddenSelections=True,
            name=f'{destination_prefix}_skinCluster'
        )[0]

    # print(f'- {source_skin = }\n- {destination_skin = }')

    # Copy skin weights
    mc.copySkinWeights(
        sourceSkin=str(source_skin),
        destinationSkin=str(destination_skin),
        surfaceAssociation=kwargs.pop('surfaceAssociation', 'closestPoint'),
        influenceAssociation=kwargs.pop('influenceAssociation', 'name'),
        noMirror=True,
        smooth=smooth,
        **kwargs
    )

    # Return result
    return graph.ls(destination_skin)[0]


def resetSkin(nodes: List[str]) -> None:
    """
    Reset the skinClusters bindPreMatrix values with the current matrix values

    Args:
        nodes: List[str], nodes to reset skin for

    """
    # TODO: upgrade to take om & cmdo types

    if isinstance(nodes, str):
        nodes = [nodes]

    for node in nodes:
        skin_clusters = history.getDeformers(node, 'skinCluster')

        if not skin_clusters:
            print(f'No skinCluster found for : {node}')
            continue

        for skin_cluster in skin_clusters:
            connections = mc.listConnections(
                f"{skin_cluster}.matrix",
                source=True, destination=False,
                plugs=True, connections=True
            )
            destinations = connections[0::2]
            sources = connections[1::2]

            for src, dest in zip(sources, destinations):
                mat = mc.getAttr(f"{src.split('.')[0]}.worldInverseMatrix")
                mc.setAttr(
                    dest.replace('matrix', 'bindPreMatrix'),
                    *mat, type='matrix'
                )


def getJointsNotInSkinHierarchy(obj_list: List[str] = None, joint_wildcard: str = '*_skn'):
    """
    Get a list of joints not in any skin of given meshes

    Args:
        obj_list: meshes to check whether they are in the skin hierarchy or not
        joint_wildcard: wildcard string for searching joints

    Returns: list of joints not in the skin hierarchy

    """
    skin_hierarchy = set()

    def filter_func(joint):
        """
        Filter joints not in given hierarchy and not connected to a skinCluster
        """
        connection = mc.listConnections(
            joint, source=False, destination=True, type='skinCluster'
        )
        return joint not in skin_hierarchy and connection is None

    if obj_list is None:
        obj_list = mc.ls(selection=True)

    elif not isinstance(obj_list, list):
        obj_list = [obj_list]

    for obj in obj_list:
        influences = mc.skinCluster(obj, query=True, influence=True)

        # build skin hierarchy list
        for influence in influences:
            if influence in skin_hierarchy:
                continue

            skin_hierarchy.update(
                set(hierarchy.getHierarchyRoot(influence))
            )

    skeleton = mc.ls(joint_wildcard, type='joint')

    joints_not_in_skin = list(
        filter(filter_func, skeleton)
    )

    return graph.ls(joints_not_in_skin)
