from typing import List, Union

from maya import cmds


__all__: List[str] = [
    'duplicateUVSet',
    'transferUVSets',
    'checkOverlappingUVs',
]


def duplicateUVSet(source_obj: str, source_uv_set: str, new_uv_set: str) -> None:
    """
    Duplicate an uv_set on an object and give it a new name

    :param source_obj: str, the object to duplicate uv set on
    :param source_uv_set: str, the name of the uv set to duplicate
    :param new_uv_set: str, the name of the duplicated uv set
    """

    cmds.polyUVSet(source_obj, uvSet=source_uv_set, copy=True, newUVSet=new_uv_set)
    cmds.polyUVSet(source_obj, currentUVSet=True, uvSet=new_uv_set)


def transferUVSets(source_obj: str, target_obj: str, keep_history: bool = False) -> Union[str, None]:
    """
    Transfer uv sets from one object to another

    :param source_obj: str, the object with the uv set to transfer
    :param target_obj: str, the object to receive the uv set
    :param keep_history: bool, whether to delete history or not

    :return: Union[str, None], the transfer node or None
    """

    source_vtx_count = len(cmds.ls(f'{source_obj}.vtx[*]', flatten=True))
    target_vtx_count = len(cmds.ls(f'{target_obj}.vtx[*]', flatten=True))
    if source_vtx_count != target_vtx_count:
        cmds.error(
            f'Trying to transfer UVs between different topologies'
            f'\n\t{source_obj} vertex count : {source_vtx_count}'
            f'\n\t{target_obj} vertex count : {target_vtx_count}'
        )

    polyTransferNode = cmds.polyTransfer(target_obj, uvSets=True, alternateObject=source_obj)

    if not keep_history:
        cmds.bakePartialHistory(target_obj, prePostDeformers=True)
        return None

    return polyTransferNode


def checkOverlappingUVs(source_obj: str) -> List[int]:
    """
    Check overlapping uv sets on given object

    :param source_obj: str, the object with the uv set to check

    :return: list of uv point indices

    """
    all_faces = f'{source_obj}.f[*]'

    return cmds.polyUVOverlap(all_faces, overlappingComponents=True) or []

