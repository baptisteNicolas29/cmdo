from typing import List, Union, Dict, Tuple

from maya import cmds
from maya.api import OpenMaya as om


__all__: List[str] = [
    'duplicateUVSet',
    'transferUVSets',
    'checkOverlappingUVs',
    'getUVShellList',
    'selectUVShellUVs'
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


def getUVShellList(sourceObj: str, uvSets: Union[str, List, None] = None) -> Dict[str, Dict[str, Union[int, List[Tuple]]]]:
    """
    Get a list of UV shells and there corresponding UV point positions

    This is given, per UV set

    :param sourceObj: str, the name of the object to retrieve UV shells from
    :param uvSets: the name of a specific UV set, if none, all UV sets  are used

    :return: Dict[str, Dict[str, Union[int, List[Tuple]]]],
        {uvSet: {"shellCount": int, "shells": [(uvId, [u, v]), ...]}}
    """

    selList = om.MSelectionList()
    selList.add(sourceObj)

    pathToShape = selList.getDagPath(0)

    meshNode = pathToShape.fullPathName()

    if uvSets is None:
        uvSets = cmds.polyUVSet(meshNode, query=True, allUVSets=True)
    else:
        uvSets = [uvSets] if isinstance(uvSets, str) else uvSets

    allSets = {}
    for currentUVSet in uvSets:
        shapeFn = om.MFnMesh(pathToShape)
        if not shapeFn.numUVs(currentUVSet):  # check is the mesh has UVs
            continue

        Us, Vs = shapeFn.getUVs(currentUVSet)
        shellCount, shellId = shapeFn.getUvShellsIds(currentUVSet)

        shells = {}
        for i, n in enumerate(shellId):
            shells.setdefault(n, []).append((i, [Us[i], Vs[i]]))

        allSets[currentUVSet] = {'shellCount': shellCount, 'shells': shells}

    return allSets


def selectUVShellUVs(sourceObj: str, uvSet: str, shellIndex: int) -> None:
    """
    Select the UVs of the given objet from the given UV set and the shell number

    :param sourceObj: str, the object to select UVs on
    :param uvSet: str, the name of the UV set
    :param shellIndex: int, the index of the UV shell

    """
    uvShells = getUVShellList(sourceObj, uvSet)

    cmds.select(*list(map(
        lambda t: f'{sourceObj}.map[{t[0]}]',
        uvShells[uvSet]['shells'][shellIndex]
    )))
