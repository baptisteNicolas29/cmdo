from typing import List, Union

from maya import cmds


__all__: List[str] = [
    'duplicateUVSet',
    'transferUVSets',
    'checkOverlappingUVs',
]


def duplicateUVSet(sourceObj: str, sourceUVSet: str, newUVSet: str) -> None:
    """
    Duplicate an uv_set on an object and give it a new name

    :param sourceObj: str, the object to duplicate uv set on
    :param sourceUVSet: str, the name of the uv set to duplicate
    :param newUVSet: str, the name of the duplicated uv set
    """

    cmds.polyUVSet(sourceObj, uvSet=sourceUVSet, copy=True, newUVSet=newUVSet)
    cmds.polyUVSet(sourceObj, currentUVSet=True, uvSet=newUVSet)


def transferUVSets(sourceObj: str, targetObj: str, keepHistory: bool = False) -> Union[str, None]:
    """
    Transfer uv sets from one object to another

    :param sourceObj: str, the object with the uv set to transfer
    :param targetObj: str, the object to receive the uv set
    :param keepHistory: bool, whether to delete history or not

    :return: Union[str, None], the transfer node or None
    """

    sourceVtxCount = len(cmds.ls(f'{sourceObj}.vtx[*]', flatten=True))
    targetVtxCount = len(cmds.ls(f'{targetObj}.vtx[*]', flatten=True))
    if sourceVtxCount != targetVtxCount:
        cmds.error(
            f'Trying to transfer UVs between different topologies'
            f'\n\t{sourceObj} vertex count : {sourceVtxCount}'
            f'\n\t{targetObj} vertex count : {targetVtxCount}'
        )

    polyTransferNode = cmds.polyTransfer(targetObj, uvSets=True, alternateObject=sourceObj)

    if not keepHistory:
        cmds.bakePartialHistory(targetObj, prePostDeformers=True)
        return None

    return polyTransferNode


def checkOverlappingUVs(sourceObj: str) -> List[int]:
    """
    Check overlapping uv sets on given object

    :param sourceObj: str, the object with the uv set to check

    :return: list of uv point indices

    """
    allFaces = f'{sourceObj}.f[*]'

    return cmds.polyUVOverlap(allFaces, overlappingComponents=True) or []

