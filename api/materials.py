import os
import random

from maya import cmds as mc


__all__ = [
    'MAYA_DEFAULT_MAT',
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


MAYA_DEFAULT_MAT = 'lambert1'

NumType = float | int
ListType = list | set | tuple


def getRandomColor(min_value: NumType = 0, max_value: NumType = 100) -> list[float]:
    """
    Generate a random double3 color range for color purposes

    Args:
        min_value: float|int, the minimum value for the color range
        max_value: float|int, the maximum value for the color range

    Returns:
        list[float], a list of double3 to be used for color ranged 0-1
    """
    if not 0 <= min_value <= max_value <= 100:
        raise Exception(
            f'Min/Max values for color range need to be between 0 and 100 got,'
            f'{min_value = } - {max_value = }'
        )

    return [
        random.randrange(min_value, max_value, 1) / 100,
        random.randrange(min_value, max_value, 1) / 100,
        random.randrange(min_value, max_value, 1) / 100
    ]


def getSceneMaterials() -> list:
    """
    Get all materials in the current scene

    Returns:
        list of all the materials in the current scene
    """
    return mc.ls(materials=True)


def getShadersFromObjects(nodes: list[str] = None, **kwargs) -> dict[str: list[str]]:
    """
    Returns the shaders of the given or selected objects
    Args:
        nodes: the node to get shaders from

    Returns:
        dict[str: list[str]], dictionary holding node: materials key value pairs
    """
    materials = {}
    for node in nodes:
        mats = getShadersFromObject(node, **kwargs)
        if mats:
            materials[node] = mats

    return materials


def getShadersFromObject(node: str = None, **kwargs) -> list[str]:
    """
    Returns the shaders of the given or selected objects
    Args:
        node: the node to get shaders from

    Returns:

    """

    return mc.ls(
        mc.hyperShade(geometries=node, listMaterialNodes=True),
        **kwargs
    )


def getObjectsFromShaders(materials: list[str] = None) -> dict[str: list[str]]:
    """

    Args:
        materials:

    Returns:

    """

    objects = {}
    for material in materials:
        objs = getObjectsFromShader(material)
        if objs:
            objects[material] = objs

    return objects


def getObjectsFromShader(material: str = None) -> list[str]:
    """

    Args:
        material:

    Returns:

    """
    return mc.hyperShade(material, listGeometries=True)


def getBoundingBoxTiles(bb):
    """
    return the bounding box of the udim tile

    Args:
        bb:

    Returns:

    """
    u_minmax, v_minmax = bb

    if u_minmax[1] != int(u_minmax[1]):
        u_minmax = (u_minmax[0], u_minmax[1] + 1)

    if v_minmax[1] != int(v_minmax[1]):
        v_minmax = (v_minmax[0], v_minmax[1] + 1)

    tiles = []
    for v in range(*map(int, v_minmax)):
        for u in range(*map(int, u_minmax)):
            tiles.append((u, v))

    return tiles


def getUVUdimTiles(mesh, uv_set=None):
    """
        Return the UVs and UV tiles used by the UVs of the input mesh.

        Args:
            mesh (str): Mesh node name.
            uv_set (str): The UV set to sample. When not
                provided the current UV map is used.

        Returns:
            dict[
                shell_id: dict[
                    uvs: shell uv indices
                    tile: tile (u, v)
                ]

    """

    kwargs = {}
    if uv_set is not None:
        kwargs["uvSetName"] = uv_set

    # bb = mc.polyEvaluate(mesh, boundingBox2d=True, **kwargs)
    # tiles = getBoundingBoxTiles(bb)

    # Get the bounding box per UV shell
    uv_shells = mc.polyEvaluate(mesh, uvShell=True, **kwargs)

    uv_data = {}
    for i in range(uv_shells):
        key = str(i)
        uv_data[key] = {}

        shell_uvs = mc.polyEvaluate(mesh, uvsInShell=i, **kwargs)
        shell_bb = mc.polyEvaluate(
            shell_uvs,
            boundingBoxComponent2d=True,
            **kwargs
        )
        shell_tiles = getBoundingBoxTiles(shell_bb)

        uv_data[key]['uvs'] = shell_uvs
        uv_data[key]['tile'] = shell_tiles[0] if shell_tiles else None

    return uv_data


def uvToUdim(tile):
    """
        UV tile to UDIM number.

        Note that an input integer of 2 means it's
        the UV tile range using 2.0-3.0.

        Returns:
            int: UDIM tile number

    """
    u, v = tile
    return 1001 + u + 10 * v


def assignMaterial(faces, material_name, mat_type='lambert'):
    """
    Assign a material, creates the material if it does not exist

    Args:
        faces:
        material_name:
        mat_type:

    Returns:

    """
    material = mc.ls(material_name, type=mat_type)
    shading_engine = None
    if not material:
        material_name = mc.shadingNode(
            mat_type, name=material_name, asShader=True
        )
        shading_engine = mc.sets(
            name=f'{material_name}SG',
            empty=True,
            renderable=True,
            noSurfaceShader=True
        )
        mc.connectAttr(
            f'{material_name}.outColor',
            f'{shading_engine}.surfaceShader'
        )

    else:
        connected = mc.connectionInfo(
            f'{material[0]}.outColor',
            destinationFromSource=True
        )
        for connection in connected:

            if mc.objectType(connection) == 'shadingEngine':
                shading_engine = connection.split('.')[0]
                break

    if shading_engine is not None:
        mc.sets(faces, edit=True, forceElement=shading_engine)


def assignMaterialPerUdim(geometry_objs, exceptions=None):
    """
    Assignes a new material per UDIM associated with the object

    Args:
        geometry_objs:
        exceptions:

    Returns:

    """
    materials = []

    if not isinstance(geometry_objs, ListType):
        geometry_objs = [geometry_objs]

    for mesh in geometry_objs:

        if any(exception in mesh for exception in (exceptions or [])):
            continue

        mc.hyperShade(assign='lambert1', geometries=f'{mesh}.f[*]')

        uv_data = getUVUdimTiles(mesh)
        if not uv_data:
            mc.warning(f'{mesh = } has no UV data, skipping ...')

        for shell_id, data in uv_data.items():
            if data['uvs'] is None or data["tile"] is None:
                continue

            faces = mc.polyListComponentConversion(data['uvs'], toFace=True)

            udim_name = uvToUdim(data["tile"])
            material_name = f'UDIM_{udim_name}'
            assignMaterial(faces, material_name)

            materials.append(material_name)

    return materials


def assign_diffuse_to_material(material_list, diffuse_path):
    """
    Assign the diffuse texture to a list of materials given a folder path

    Args:
        material_list:
        diffuse_path:
    Returns:

    """
    connect_dict = {
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

    if not isinstance(material_list, ListType):
        material_list = [material_list]

    diffuse_name = os.path.basename(diffuse_path).split('.')[0]
    for material in material_list:

        color_file = mc.shadingNode(
            'file',
            asTexture=True,
            isColorManaged=True,
            name=f'{diffuse_name}_color'
        )

        mc.setAttr(
            f'{color_file}.fileTextureName',
            str(diffuse_path),
            type='string'
        )

        place_tex = mc.shadingNode(
            'place2dTexture',
            asUtility=True,
            name=f'{diffuse_name}_place2D'
        )

        # Reconnect attribute between the place2dtexture and the color file
        for source, destination in connect_dict.items():
            mc.connectAttr(
                f'{place_tex}.{source}',
                f'{color_file}.{destination}'
            )

        mc.connectAttr(
            f'{color_file}.outColor',
            f'{material}.color', force=True
        )


def addMaterialWithColor(
        objects: list[str] = None,
        random_color: bool = True,
        color: tuple[float] | list[float] = (0.249, 0.123667, 0.047808),
        color_range: tuple = (30, 60)
):
    """
    For each geometry in the current scene, assign new material
    and either a random color or given color, default color is brown

    Args:
        objects: list[str], a list of objects to assigne color to, default None
        random_color: bool, whether to select a random color or brown
        color: tuple[float] | list[float], rbg color values, defaults to brown
        color_range: tuple[float]: the range of accepted color to randomise
    """

    color = (
        getRandomColor(*color_range)
        if random_color is True or not color
        else color
    )

    materials = getShadersFromObjects(objects)

    for obj in objects:
        object_materials = materials.get(obj)

        for mat in reversed(object_materials):
            if mc.nodeType(mat) == 'GLSLShader':
                object_materials.remove(mat)

        if not object_materials or MAYA_DEFAULT_MAT in object_materials:
            print(f'Assigning material and color to: {objects}')
            materials[obj] = assignMaterialPerUdim(obj)

    material_set = []
    for mat in materials.values():
        material_set.extend(mat)

    for mat in set(material_set):

        match mc.nodeType(mat):
            case 'lambert':
                color_attr = 'color'
            case 'standardSurface':
                color_attr = 'baseColor'
            case 'usdPreviewSurface':
                color_attr = 'diffuseColor'
            case _:
                color_attr = 'color'

        if not mc.connectionInfo(f'{mat}.{color_attr}', isDestination=True):
            mc.setAttr(f'{mat}.{color_attr}', *color, type='double3')
