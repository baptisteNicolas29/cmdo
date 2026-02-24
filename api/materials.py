from typing import List, Dict, Union, Set, Tuple, Any

import os
import random
from pathlib import Path

from maya import cmds

from ..core.graphLib import Graph
from ..core.cmdoTyping import *


__all__: List[str] = [
    'MAYA_DEFAULT_MAT',
    'MAYA_LEGACY_DEFAULT_MAT',
    'getMaterialColorAttribute',
    'assignDefaultShader',
    'getRandomColor',
    'getSceneMaterials',
    'getShadersFromObject',
    'getShadersFromObjects',
    'getObjectsFromShader',
    'getObjectsFromShaders',
    'getBoundingBoxTiles',
    'getUVUdimTiles',
    'uvToUdim',
    'assignMaterial',
    'assignMaterialPerUdim',
    'addMaterialWithColor',
]


MAYA_DEFAULT_MAT = 'standardSurface1'
MAYA_LEGACY_DEFAULT_MAT = 'lambert1'

materialColorAttributes = {
    'standardSurface': 'baseColor',
    'lambert': 'color',
    'blinn': 'color',
    'phong': 'color',
    'phongE': 'color',
    'usdPreviewSurface': 'diffuseColor',
}


def getMaterialColorAttribute(material: str) -> str:
    """
    Get the name of the color attribute for the given material.

    :param material: str, the material to get the color attribute for

    :return: str, the name of the color attribute
    """

    # baseColor is the attribute of standardSurface material and
    # should be considered the default material type
    return materialColorAttributes.get(cmds.nodeType(f'{material}'), 'baseColor')


def assignDefaultShader(nodes: CmdoList) -> None:
    """
    Assign given nodes to the initial shading engine

    :param nodes: CmdoList, a list of nodes/components to add to the default shading engine
    """

    initSG = Graph.ls('initialShadingGroup')[0]

    initSG.addMembers(nodes)


def getRandomColor(minValue: int = 0, maxValue: int = 100) -> List[float]:
    """
    Generate a random double3 color range for color purposes

    :param minValue: CmdoNumber, the minimum value for the color range
    :param maxValue: CmdoNumber, the maximum value for the color range

    :return: list[float], a list of double3 to be used for color ranged 0-1
    """

    if not 0 <= minValue <= maxValue <= 100:
        raise Exception(
            f'Min/Max values for color range need to be between 0 and 100 got,'
            f'{minValue = } - {maxValue = }'
        )

    return [
        random.randrange(minValue, maxValue, 1) / 100,
        random.randrange(minValue, maxValue, 1) / 100,
        random.randrange(minValue, maxValue, 1) / 100
    ]


def getSceneMaterials() -> Graph:
    """
    Get all materials in the current scene

    :return: List, list of all the materials in the current scene
    """

    return Graph.ls(materials=True)


def getShadersFromObjects(nodes: CmdoList, **kwargs) -> Dict[str, Graph]:
    """
    Returns the shaders of the given or selected objects

    :param nodes: CmdoList, the node to get shaders from

    :return: dict[str: list[str]], dictionary holding {node: materials} pairs
    """

    materials = {}
    for node in Graph.ls(nodes):
        mats = getShadersFromObject(node, **kwargs)
        if mats:
            materials[node] = mats

    return materials


def getShadersFromObject(node: str = None, **kwargs) -> Graph:
    """
    Returns the shaders of the given or selected objects

    :param node: str, the node to get shaders from

    :return: List[str], list of all the materials assigned to given object
    """

    if not isinstance(node, str):
        node = Graph.ls(node)[0].name

    return Graph.ls(
        *cmds.hyperShade(geometries=node, listMaterialNodes=True),
        **kwargs
    )


def getObjectsFromShaders(materials: List[str] = None) -> Dict[str, Graph]:
    """
    Returns the objects to which the given materials are assigned

    :param materials: List[str], list of materials to get objects from

    :return: dict[str: list[str]], dictionary holding {material: nodes} pairs
    """

    objects = {}
    for material in materials:
        objects[material] = getObjectsFromShader(material) or Graph()

    return objects


def getObjectsFromShader(material: str = None) -> Graph:
    """
    Returns the objects to which the given material is assigned

    :param material: str, the material to get objects from

    :return: list[str], list of all object the given material is assigned
    """

    return Graph.ls(*cmds.hyperShade(listGeometries=material))


def getBoundingBoxTiles(boundingBox2D:  Tuple[Tuple[float, float], Tuple[float, float]]) -> List[Tuple[int, int]]:
    """
    Get the bounding box of the UDIM tile

    :param boundingBox2D: Tuple[Tuple[float, float], Tuple[float, float]], the UV coordinates of the 2D bounding box

    :return: List[Tuple[int, int]], the bounding box of the UDIM tile
    """

    uMinMax, vMinMax = boundingBox2D

    if uMinMax[1] != int(uMinMax[1]):
        uMinMax = (uMinMax[0], uMinMax[1] + 1)

    if vMinMax[1] != int(vMinMax[1]):
        vMinMax = (vMinMax[0], vMinMax[1] + 1)

    tiles = []
    for v in range(*map(int, vMinMax)):
        for u in range(*map(int, uMinMax)):
            tiles.append((u, v))

    # tiles -> [(uTileIndex, vTileIndex)], List[Tuple[int, int]]
    return tiles


def getUVUdimTiles(mesh: str, uvSet: str = None) -> Dict[Any, Any]:
    """
    Return the UVs and UV tiles used by the UVs of the input mesh.

    :param mesh: str, mesh node name
    :param uvSet: str, the UV set to sample. When not provided the current UV map is used.

    :return: dict[shellID: dict[uvs: shell uv indices, tile: tile (u, v)]
    """

    kwargs = {}
    if uvSet is not None:
        kwargs["uvSetName"] = uvSet

    # bb = cmds.polyEvaluate(mesh, boundingBox2d=True, **kwargs)
    # tiles = getBoundingBoxTiles(bb)

    # Get the bounding box per UV shell
    uvShells = cmds.polyEvaluate(f'{mesh}', uvShell=True, **kwargs)

    uvData = {}
    for i in range(uvShells):
        key = str(i)
        uvData[key] = {}

        shellUVs = cmds.polyEvaluate(f'{mesh}', uvsInShell=i, **kwargs)
        shellBBx = cmds.polyEvaluate(
            shellUVs,
            boundingBoxComponent2d=True,
            **kwargs
        )
        shellTiles = getBoundingBoxTiles(shellBBx)

        uvData[key]['uvs'] = shellUVs
        uvData[key]['tile'] = shellTiles[0] if shellTiles else None

    # uvData -> {shellIndex: {uvVertexIndices, tileCoordinates}}
    #  Dict[str: Dict[str: List[str], str: Tuple[int, int]]]

    return uvData


def uvToUdim(tile: Tuple[int, int]) -> int:
    """
    UV tile to UDIM number

    exemples:
        uv tile (0, 0) -> 1001
        uv tile (0, 1) -> 1011
        uv tile (1, 1) -> 1012

    Note that an input integer of 2 means it's the UV tile range using 2.0-3.0.

    :param tile: Tuple[int, int], the UV tile origin coordinates

    :return: int: UDIM tile number
    """

    u, v = tile
    return 1001 + u + 10 * v


def assignMaterial(faces: Union[str, List[str]], materialName: str, materialType: str = 'standardSurface') -> Graph:
    """
    Assign a material, creates the material if it does not exist

    :param faces: Union[str, List[str]], the mesh or mesh components to assign the material to
    :param materialName: str, the name of the material to assign or create
    :param materialType: str, the type of the material to create if needed

    :return: Tuple[str, str], the material name and the shading engine attached to it
    """

    material = cmds.ls(materialName, type=materialType)
    shadingEngine = None
    if not material:
        material = cmds.shadingNode(
            materialType, name=materialName, asShader=True
        )
        print(f'From shadingNode - {material}')
        shadingEngine = cmds.sets(
            name=f'{material}SG',
            empty=True,
            renderable=True,
            noSurfaceShader=True
        )
        cmds.connectAttr(
            f'{material}.outColor',
            f'{shadingEngine}.surfaceShader'
        )
    else:
        material = material[0]
        connected = cmds.connectionInfo(
            f'{material}.outColor',
            destinationFromSource=True
        )
        for connection in connected:

            if cmds.objectType(connection) == 'shadingEngine':
                shadingEngine = connection.split('.')[0]
                break

    if shadingEngine is not None:
        cmds.sets(faces, edit=True, forceElement=shadingEngine)

    print(f'{material = }, {shadingEngine = }')
    return Graph.ls(*[material, shadingEngine])


def assignMaterialPerUdim(geometryObjects: Union[Graph, List[str]], exceptions: List[str] = None) -> Graph:
    """
    Assignes a new material per UDIM associated with the object

    :param geometryObjects: the object to assign materials per UDIM to
    :param exceptions: list of meshes to skip

    :return: Graph, the list of new materials
    """

    materials = Graph()
    if not isinstance(geometryObjects, (list, tuple, Graph)):
        geometryObjects = Graph.ls(geometryObjects)

    for mesh in geometryObjects:

        if any(exception in mesh.name for exception in list(exceptions or [])):
            continue

        cmds.hyperShade(
            assign=MAYA_LEGACY_DEFAULT_MAT,
            geometries=f'{mesh}.f[*]'
        )

        uvData = getUVUdimTiles(mesh)
        if not uvData:
            cmds.warning(f'{mesh = } has no UV data, skipping ...')

        for shellID, data in uvData.items():
            if data['uvs'] is None or data["tile"] is None:
                continue

            faces = cmds.polyListComponentConversion(data['uvs'], toFace=True)

            udimName = uvToUdim(data["tile"])
            materialName = f'UDIM_{udimName}'
            material = assignMaterial(faces, materialName)  # shadingEngine
            print(f'\n{material = }')

            materials.extend(material)

    return materials


def assignDiffuseToMaterial(material: str, diffusePath: Union[Path, str]) -> None:
    """
    Assign the diffuse texture to a list of materials given a file path

    :param material: the material to assign a diffuse file to
    :param diffusePath: the path to the diffuse file

    """

    connectDict = {
        'coverage': 'coverage',
        'translateFrame': 'translateFrame',
        'rotateFrame': 'rotateFrame',
        'mirrorU': 'mirrorU',
        'mirrorV': 'mirrorV',
        'stagger': 'stagger',
        'wrapU': 'wrapU',
        'wrapV': 'wrapV',
        'repeatUV': 'repeatUV',
        'offset': 'offset',
        'rotateUV': 'rotateUV',
        'noiseUV': 'noiseUV',
        'vertexUvOne': 'vertexUvOne',
        'vertexUvTwo': 'vertexUvTwo',
        'vertexUvThree': 'vertexUvThree',
        'vertexCameraOne': 'vertexCameraOne',
        'outUV': 'uv',
        'outUvFilterSize': 'uvFilterSize'
    }

    diffuseName = Path(diffusePath).name

    colorFile = cmds.shadingNode(
        'file',
        asTexture=True,
        isColorManaged=True,
        name=f'{diffuseName}_color'
    )

    cmds.setAttr(
        f'{colorFile}.fileTextureName',
        str(diffusePath),
        type='string'
    )

    placeTextureNode = cmds.shadingNode(
        'place2dTexture',
        asUtility=True,
        name=f'{diffuseName}_place2D'
    )

    # Reconnect attribute between the place2dtexture and the color file
    for source, destination in connectDict.items():
        cmds.connectAttr(
            f'{placeTextureNode}.{source}',
            f'{colorFile}.{destination}'
        )

    diffuseAttrName = getMaterialColorAttribute(material)
    cmds.connectAttr(
        f'{colorFile}.outColor',
        f'{material}.{diffuseAttrName}', force=True
    )


def addMaterialWithColor(
        objects: List[str] = None,
        random_color: bool = True,
        color: Union[Tuple[float], List[float]] = (0.249, 0.123667, 0.047808),
        color_range: Tuple = (30, 60)
 ) -> None:
    """
    For each geometry in the current scene, assign new material

    and either a random color or given color, default color is brown

    :param objects: list[str], a list of objects to assigne color to, default None
    :param random_color: bool, whether to select a random color or brown
    :param color: Union[Tuple[float], List[float]], rbg color values, defaults to brown
    :param color_range: tuple[float]: the range of accepted color to randomise
    """

    color = (
        getRandomColor(*color_range)
        if random_color is True or not color
        else color
    )

    materials = getShadersFromObjects(objects or None)

    for obj in objects:
        objectMaterials = materials.get(obj)

        for i, mat in reversed(list(enumerate(objectMaterials))):
            if cmds.nodeType(f'{mat}') == 'GLSLShader':
                objectMaterials.pop(i)

        if not objectMaterials or MAYA_DEFAULT_MAT in objectMaterials.getSelectionStrings():
            print(f'Assigning material and color to: {objects}')
            materials[obj] = Graph.ls(assignMaterialPerUdim(obj))

    materialSet = []
    for mat in materials.values():
        materialSet.extend(mat)

    for mat in set(materialSet):
        colorAttr = getMaterialColorAttribute(mat)

        if not cmds.connectionInfo(f'{mat}.{colorAttr}', isDestination=True):
            cmds.setAttr(f'{mat}.{colorAttr}', *color, type='double3')
