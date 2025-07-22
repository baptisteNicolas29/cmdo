from typing import List, Union, Sequence, Optional, Type

from maya import cmds as mc, mel
from maya.api import OpenMaya as om

from .abstract import dg_lib, dag_lib


# TODO: probably remove / rework all of this


#  MFnNurbsSurface
def int_to_form(
        form: int
) -> int:

    """
    Retourne la forme de la surface.

    Parameters
    ----------
    form : int
        Forme de la surface.

    Returns
    -------
    int
        Forme de la surface.
    """

    if form == 0:
        return om.MFnNurbsSurface.kInvalid
    elif form == 1:
        return om.MFnNurbsSurface.kOpen
    elif form == 2:
        return om.MFnNurbsSurface.kClosed
    elif form == 3:
        return om.MFnNurbsSurface.kPeriodic
    else:
        raise RuntimeError(
            "La forme de la surface n'est pas valide.")


#  MVectors
def to_mvector(
    vector: Union[
        om.MVector,
        List[float],
        float
    ]
) -> om.MVector:

    """
    Convertit les données de vecteur en MVector.

    Args:
        vector: Union[
            om.MVector,
            List[float],
            float
        ]:
            Les données de vecteur à convertir.

    Returns:
        om.MVector:
            Les données de vecteur converties en MVector.
    """

    if isinstance(vector, om.MVector):
        return vector

    if isinstance(vector, list):
        return om.MVector(vector)

    if isinstance(vector, float):
        return om.MVector(vector, vector, vector)


#  MPointArray
def to_mpointarray(
    points: Union[
        om.MPointArray,
        List[om.MPoint],
        List[List[float]]
    ]
) -> om.MPointArray:

    """
    Convertit les données de points en MPointArray.

    Parameters
    ----------
    points : Union[om.MPointArray, List[om.MPoint], List[List[float]]]
        Les données de points à convertir.

    Returns
    -------
    om.MPointArray
        Les données de points converties en MPointArray.
    """

    if (
        isinstance(points, om.MPointArray)
        or (
            isinstance(points, list)
            and all(isinstance(p, om.MPoint)
                    for p in points))
    ):

        pass

    elif (
        isinstance(points, (list, tuple))
        and all(isinstance(p, (list, tuple))
                and len(p) in (3, 4)
                for p in points)
    ):

        points = om.MPointArray([
            om.MPoint(
                point[0], point[1], point[2])
            for point in points])

    else:
        raise TypeError("Invalid points format")

    return points


def mpointarray_to_list(
    array: om.MPointArray
) -> List[List[float]]:

    """
    Convertit les données de MPointArray en liste.

    Args:
        array (om.MPointArray):
            Les données à convertir.

    Returns:
        List[List[float]]:
            Les données converties en liste.
    """

    return [
        [point.x, point.y, point.z, point.w]
        for point in array
    ]


#  MDoubleArray
def to_MDoubleArray(
    knots: Union[
        om.MDoubleArray,
        Sequence[float]
    ]
) -> om.MDoubleArray:

    """
    Convertit les données de knots en MDoubleArray.

    Parameters
    ----------
    knots : Union[om.MDoubleArray, Sequence[float]]
        Les données de knots à convertir.

    Returns
    -------
    om.MDoubleArray
        Les données de knots converties en MDoubleArray.
    """

    if isinstance(knots, om.MDoubleArray):
        return knots

    elif isinstance(knots, Sequence) and all(isinstance(k, float) for k in knots):
        return om.MDoubleArray(knots)

    else:
        return om.MDoubleArray()


def mdoublearray_to_list(
    array: om.MDoubleArray
) -> List[float]:

    """
    Convertit les données de MDoubleArray en liste.

    Args:
        array (om.MDoubleArray):
            Les données à convertir.

    Returns:
        List[float]:
            Les données converties en liste.
    """

    return list(array)


# MMMatrix
def to_MMatrix(
    matrix: Union[
        om.MMatrix,
        List[List[float]],
        List[float]
    ]
) -> om.MMatrix:

    """
    Convertit une matrice en 'om.MMatrix'.

    Args:
        matrix (Union[om.MMatrix, List[List[float]], List[float]]):
            La matrice à convertir.

    Returns:
        om.MMatrix:
            La matrice convertie en 'om.MMatrix'.
    """

    if isinstance(matrix, om.MMatrix):
        return matrix

    if isinstance(matrix, List) and all(
        isinstance(value, float) for value in matrix
    ):
        return om.MMatrix(matrix)

    if isinstance(matrix, List) and all(
        isinstance(value, List) for value in matrix
    ):
        return om.MMatrix(matrix)

    raise TypeError("Invalid matrix format.")


def to_MMatrixArray(
    matrices: Union[
        om.MMatrixArray,
        List[om.MMatrix],
        List[List[float]],
        List[float]
    ]
) -> om.MMatrixArray:

    """
    Convertit une liste de matrices en 'om.MMatrixArray'.

    Args:
        matrices (Union[
            om.MMatrixArray,
            List[om.MMatrix],
            List[List[float]],
            List[float]
        ]):
            La liste de matrices à convertir.

    Returns:
        om.MMatrixArray:
            La liste de matrices convertie en 'om.MMatrixArray'.
    """

    if isinstance(matrices, om.MMatrixArray):
        return matrices

    mmatrix_array = om.MMatrixArray()

    if isinstance(matrices, om.MMatrix):
        mmatrix_array.append(matrices)

    if (
        isinstance(matrices, List)
        and all(isinstance(value, float) for value in matrices)
    ):
        mmatrix_array.append(om.MMatrix(matrices))

    if (
        isinstance(matrices, List)
        and all(isinstance(value, om.MMatrix) for value in matrices)
    ) or (
        isinstance(matrices, List)
        and all(isinstance(value, List) for value in matrices)
        and all(isinstance(value, float) for value in matrices[0])
    ):
        for matrix in matrices:
            mmatrix_array.append(matrix)

    return mmatrix_array


def MMatrix_to_list(
    matrix: om.MMatrix
) -> List[float]:

    """
    Convertit une matrice en liste.

    Args:
        matrix (om.MMatrix):
            La matrice à convertir.

    Returns:
        List[float]:
            La matrice convertie en liste.
    """

    return [
        matrix[i] for i in range(16)
    ]


# MPlug
def to_MPlugArrays_list(
    output_plugs: Optional[Union[
        List[om.MPlugArray],
        List[List[om.MPlug]],
        List[List[str]],
        om.MPlugArray,
        List[om.MPlug],
        List[str],
        om.MPlug,
        str
        ]] = None
) -> Optional[List[om.MPlugArray]]:

    """
    Convertit les plugs de sortie en plugs Maya.

    Args:
        output_plugs (Optional[Union[
            List[om.MPlugArray],
            List[List[om.MPlug]],
            List[List[str]],
            om.MPlugArray,
            List[om.MPlug],
            List[str],
            om.MPlug,
            str
        ]]):
            Les plugs de sortie.

    Returns:
        Optional[List[om.MPlugArray]]:
            Les plugs de sortie convertis en plugs Maya.
    """

    if (
        output_plugs is None
        or (
            isinstance(output_plugs, list)
            and all(
                isinstance(array, om.MPlugArray)
                for array in output_plugs
            )
        )
    ):

        return output_plugs

    if (
        isinstance(output_plugs, list)
        and all(isinstance(array, list) for array in output_plugs)
        and all(
            all(isinstance(plug, om.MPlug) for plug in array)
            for array in output_plugs
        )
    ):

        return [
            om.MPlugArray(plugs)
            for plugs in output_plugs
        ]

    if (
        isinstance(output_plugs, list)
        and all(isinstance(array, list) for array in output_plugs)
        and all(
            all(isinstance(plug, str) for plug in array)
            for array in output_plugs
        )
    ):
        return [
            om.MPlugArray([
                dg_lib.DGNode(plug.split(".")[0]).plugs.get_plug(
                    ".".join(plug.split(".")[1:])
                )
                for plug in plugs
            ])
            for plugs in output_plugs
        ]

    if isinstance(output_plugs, om.MPlugArray):
        return [output_plugs]

    if (
        isinstance(output_plugs, list)
        and all(isinstance(plug, om.MPlug) for plug in output_plugs)
    ):
        return [om.MPlugArray(output_plugs)]

    if (
        isinstance(output_plugs, list)
        and all(isinstance(plug, str) for plug in output_plugs)
    ):
        return [
            om.MPlugArray([
                dg_lib.DGNode(plug.split(".")[0]).plugs.get_plug(
                    ".".join(plug.split(".")[1:])
                )
                for plug in output_plugs
            ])
        ]

    if isinstance(output_plugs, str):
        return [
            om.MPlugArray([
                dg_lib.DGNode(
                    output_plugs.split(".")[0]).plugs.get_plug(
                    ".".join(output_plugs.split(".")[1:])
                )
            ])
        ]


def to_MPlugArray(
    to_convert: Optional[Union[
        om.MPlugArray,
        List[om.MPlug],
        List[str],
        om.MPlug,
        str
    ]]
) -> om.MPlugArray:

    """
    Convertit les plugs en MPlugArray.

    Args:
        to_convert (Optional[Union[
            om.MPlugArray,
            List[om.MPlug],
            List[str],
            om.MPlug,
            str
        ]]):
            Les plugs de sortie.

    Returns:
        om.MPlugArray:
            Les plugs de sortie convertis en plugs Maya.
    """

    if (
        to_convert is None
        or isinstance(to_convert, om.MPlugArray)
    ):
        return to_convert

    if (
        isinstance(to_convert, list)
        and all(isinstance(plug, om.MPlug) for plug in to_convert)
    ):
        return om.MPlugArray(to_convert)

    if (
        isinstance(to_convert, list)
        and all(isinstance(plug, str) for plug in to_convert)
    ):
        return om.MPlugArray([
            dg_lib.DGNode(plug.split(".")[0]).plugs.get_plug(
                ".".join(plug.split(".")[1:])
            )
            for plug in to_convert
        ])

    if isinstance(to_convert, om.MPlug):
        return om.MPlugArray([to_convert])

    if isinstance(to_convert, str):
        return om.MPlugArray([
            dg_lib.DGNode(to_convert.split(".")[0]).plugs.get_plug(
                ".".join(to_convert.split(".")[1:])
            )
        ])


def to_MPlug(
    to_convert: Union[
        om.MPlug,
        str
    ]
) -> om.MPlug:

    """
    Convertit les plugs en MPlug.

    Args:
        to_convert (Union[om.MPlug, str]):
            Les plugs de sortie.

    Returns:
        om.MPlug:
            Les plugs de sortie convertis en plugs Maya.
    """

    if isinstance(to_convert, om.MPlug):
        return to_convert

    if isinstance(to_convert, str):
        return dg_lib.DGNode(to_convert.split(".")[0]).plugs.get_plug(
            ".".join(to_convert.split(".")[1:])
        )


# MObject
def geometries_to_mObjectArray(
    geometries: Optional[Union[
        om.MObjectArray,
        List[om.MObject],
        List[Type[dg_lib.DGNode]],
        List[str],
        om.MObject,
        Type[dg_lib.DGNode],
        str
    ]] = None
) -> om.MObjectArray:

    """
    Convertit les géométries spécifiées en MObjectArray.

    Args:
        geometries (Optional[Union[
            om.MObjectArray,
            List[om.MObject],
            List[Type[dg_lib.DGNode]],
            List[str],
            om.MObject,
            Type[dg_lib.DGNode],
            str
        ]]):
            Les géométries à valider.

    Returns:
        om.MObjectArray:
            La liste des géométries validées.
    """

    if geometries is None:

        return om.MObjectArray()

    if isinstance(geometries, str):

        return om.MObjectArray(
            [dag_lib.DAGNode(geometries).maya_object]
        )

    elif isinstance(geometries, dg_lib.DGNode):

        return om.MObjectArray(
            [geometries.maya_object]
        )

    elif (
        isinstance(geometries, list)
        and all(
            isinstance(geo, str)
            for geo in geometries
        )
    ):

        return om.MObjectArray(
            [dg_lib.DGNode(geo).maya_object for geo in geometries]
        )

    elif (
        isinstance(geometries, list)
        and all(
            isinstance(geo, dg_lib.DGNode)
            for geo in geometries
        )
    ):

        return om.MObjectArray(
            [geo.maya_object for geo in geometries]
        )

    elif (
        isinstance(geometries, om.MObject)
        or (
            isinstance(geometries, list)
            and all(
                isinstance(geo, om.MObject)
                for geo in geometries
            )
        )
    ):

        return om.MObjectArray([geometries])

    elif not isinstance(geometries, om.MObjectArray):

        raise TypeError(
            "Error while setting input geometries."
            f"\n - value type: {type(geometries)}"
            "\n - is not supported."
            f"\n - Actual type: {type(geometries).__name__}"
        )
    return None


def to_MObjectArray(
    list_mobjects: Optional[Union[
        om.MObjectArray,
        List[om.MObject],
        List[str],
        om.MObject,
        str
    ]] = None
) -> om.MObjectArray:

    """
    Convertit les MObjects en MObjectArray.

    Args:
        list_mobjects (Optional[Union[
            om.MObjectArray,
            List[om.MObject],
            List[str],
            om.MObject,
            str
        ]]):
            Les MObjects à convertir.

    Returns:
        om.MObjectArray:
            Les MObjects convertis en MObjectArray.
    """

    if list_mobjects is None:
        return om.MObjectArray()

    if isinstance(list_mobjects, om.MObjectArray):
        return list_mobjects

    if isinstance(list_mobjects, om.MObject):
        return om.MObjectArray([list_mobjects])

    if isinstance(list_mobjects, str):
        return om.MObjectArray(
            [dg_lib.DGNode(list_mobjects).maya_object]
        )

    if (
        isinstance(list_mobjects, list)
        and all(isinstance(mobject, om.MObject) for mobject in list_mobjects)
    ):
        return om.MObjectArray(list_mobjects)

    if (
        isinstance(list_mobjects, list)
        and all(isinstance(mobject, str) for mobject in list_mobjects)
    ):
        return om.MObjectArray([
            dg_lib.DGNode(mobject).maya_object
            for mobject in list_mobjects
        ])


# MDagPath
def geometries_to_mdagpath_array(
    geometries: Union[
        om.MDagPathArray,
        om.MObjectArray,
        List[om.MDagPath],
        List[om.MObject],
        List[Type[dag_lib.DAGNode]],
        List[str],
        om.MDagPath,
        om.MObject,
        Type[dag_lib.DAGNode],
        str
    ]
) -> om.MDagPathArray:

    """
    Convertit les géométries spécifiées en MDagPathArray.

    Args:
        geometries (
            Union[
                om.MDagPathArray,
                om.MObjectArray,
                List[om.MDagPath],
                List[om.MObject],
                List[Type[dag_lib.DAGNode]],
                List[str],
                om.MDagPath,
                om.MObject,
                Type[dag_lib.DAGNode],
                str
            ]
        ):
            Les géométries à convertir.

    Returns:
        om.MDagPathArray
    """

    if isinstance(geometries, str):

        return om.MDagPathArray(
            [dag_lib.DAGNode(geometries).maya_dagPath]
        )

    elif isinstance(geometries, dag_lib.DAGNode):

        return om.MDagPathArray(
            [geometries.maya_dagPath]
        )

    elif isinstance(geometries, om.MDagPath):

        return om.MDagPathArray(
            [geometries]
        )

    elif isinstance(geometries, om.MObject):

        return om.MDagPathArray([
            dag_lib.DAGNode(
                om.MFnDependencyNode(geometries).name()
            ).maya_dagPath
        ])

    elif (
        isinstance(geometries, list)
        and all(isinstance(geo, str) for geo in geometries)
    ):

        return om.MDagPathArray(
            [
                dag_lib.DAGNode(geo).maya_dagPath
                for geo in geometries
            ]
        )

    elif (
        isinstance(geometries, list)
        and all(
            isinstance(geo, dag_lib.DAGNode)
            for geo in geometries
        )
    ):

        return om.MDagPathArray(
            [geo.maya_dagPath for geo in geometries]
        )

    elif (
        isinstance(geometries, list)
        and all(isinstance(geo, om.MDagPath) for geo in geometries)
    ):

        return om.MDagPathArray(
            geometries
        )

    elif (
        isinstance(geometries, list)
        and all(isinstance(geo, om.MObject) for geo in geometries)
    ) or (
        isinstance(geometries, om.MObjectArray)
    ):

        return om.MDagPathArray(
            [
                dag_lib.DAGNode(
                    om.MFnDependencyNode(geo).name()
                ).maya_dagPath
                for geo in geometries
            ]
        )

    elif isinstance(geometries, om.MDagPathArray):

        return geometries

    else:

        raise TypeError(
            f"Invalid geometries type: {type(geometries).__name__}"
        )


def check_remove_mesh_instances(obj: str) -> Union[str, None]:
    """
    Check the passed object makes it unique
    removes history and renames the shape
    Args:
        obj: the object name to check or None if a problem occurred

    Returns:
        the name of the shape of the object
    """
    if not mc.objExists(obj):
        mc.warning(f'Given obj does not exist : {obj}. Aborting....')
        return

    mc.bakePartialHistory(obj, prePostDeformers=True)

    shapes = mc.listRelatives(obj, c=True, s=True, f=True)
    if not shapes:
        mc.warning(f'Given obj has no shapes : {obj}. Aborting....')
        return

    if len(mc.listRelatives(shapes, ap=True)) > 1:
        mc.select(obj)
        mel.eval('ConvertInstanceToObject()')

    new_shape_name = mc.rename(
        mc.listRelatives(obj, c=True, s=True, f=True)[0],
        f'{obj}Shape'
    )

    return new_shape_name
