from typing import List

from maya import cmds


__all__: List[str] = [
    'duplicateUVSet',
    'transferUVSets',
    'checkOverlappingUVs',
]


def duplicateUVSet(source_obj, source_uv_set, new_uv_set):
    """
    Duplicate an uv_set on an object and give it a new name

    Args:
        source_obj: the object to duplicate uv set on
        source_uv_set: the name of the uv set to duplicate
        new_uv_set: the name of the duplicated uv set

    """
    cmds.polyUVSet(source_obj, uvSet=source_uv_set, copy=True, newUVSet=new_uv_set)
    cmds.polyUVSet(source_obj, currentUVSet=True, uvSet=new_uv_set)


def transferUVSets(source_obj, target_obj, keep_history=False):
    """
    Transfer uv sets from one object to another

    Args:
        source_obj: the object with the uv set to transfer
        target_obj: the object to receive the uv set
        keep_history: whether to delete history or not

    """
    source_vtx_count = len(cmds.ls(f'{source_obj}.vtx[*]', flatten=True))
    target_vtx_count = len(cmds.ls(f'{target_obj}.vtx[*]', flatten=True))
    if source_vtx_count != target_vtx_count:
        cmds.error(
            f'Trying to transfer UVs between different topologies'
            f'\n\t{source_obj} vertex count : {source_vtx_count}'
            f'\n\t{target_obj} vertex count : {target_vtx_count}'
        )

    cmds.polyTransfer(target_obj, uvSets=True, alternateObject=source_obj)

    if not keep_history:
        cmds.bakePartialHistory(target_obj, prePostDeformers=True)


def checkOverlappingUVs(source_obj):
    """


    Args:
        source_obj:

    Returns:

    """
    all_faces = f'{source_obj}.f[*]'

    return cmds.polyUVOverlap(all_faces, overlappingComponents=True) or []

