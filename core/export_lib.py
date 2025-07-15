from typing import Union

# import json
# import numpy as np

from maya.api import OpenMaya as om


# TODO: MOVE TO ANOTHER LIBRARY "RIG"
print(
    DeprecationWarning(
        'export_lib is deprecated in cmdo, '
        'it will be moved to a library for rigging'
    )
)

# def export_list_to_json(
#     list: list,
#     name: str,
#     path: str = None
# ) -> None:
#
#     """
#     Exporte une liste en json
#
#     Args:
#         list (list):
#             liste à exporter
#
#         name (str):
#             nom du fichier
#
#         path (str, optional):
#             chemin du fichier. Defaults to None.
#
#     Returns:
#         None
#     """
#
#     path = f"{path}/{name}" if path else name
#
#     with open(f"{path}.json", "w") as _file:
#         json.dump(list, _file)
#
#
# def export_dict_to_json(
#     dict: dict,
#     name: str,
#     path: str = None
# ) -> None:
#
#     """
#     Exporte un dictionnaire en json
#
#     Args:
#         dict (dict):
#             dictionnaire à exporter
#
#         name (str):
#             nom du fichier
#
#         path (str, optional):
#             chemin du fichier. Defaults to None.
#
#     Returns:
#         None
#     """
#
#     path = f"{path}/{name}" if path else name
#
#     with open(f"{path}.json", "w") as _file:
#
#         json.dump(
#             dict,
#             _file,
#             indent=4,
#             separators=(",", ":")
#         )
#
#
# def import_dict_from_json(
#     name: str,
#     path: str = None
# ) -> dict:
#
#     """
#     Lit un dictionnaire depuis un fichier json
#
#     Args:
#         name (str):
#             nom du fichier
#
#         path (str, optional):
#             chemin du fichier. Defaults to None.
#
#     Returns:
#         dict
#             Le dictionnaire lu
#     """
#
#     path = f"{path}/{name}" if path else name
#
#     with open(f"{path}.json") as _file:
#         return json.load(_file)
#
#
# def export_MArray_to_binary(
#     list: Union[om.MDoubleArray, om.MIntArray],
#     name: str,
#     path: str = None,
#     compressed: bool = False
# ) -> None:
#
#     """
#     Exporte une liste initialement de type MDoubleArray ou MIntArray
#     en binaire
#
#     Args:
#         list (Union[om.MDoubleArray, om.MIntArray]):
#             liste à exporter
#
#         name (str):
#             nom du fichier
#
#         path (str, optional):
#             chemin du fichier. Defaults to None.
#
#         compressed (bool, optional):
#             si True, le fichier est compressé.
#             Defaults to False.
#
#     Returns:
#         None
#     """
#
#     path = f"{path}/{name}" if path else name
#
#     double_array = np.array(list, dtype=np.float64)
#
#     if not compressed:
#         double_array.tofile(f"{path}.bin")
#     else:
#         np.savez_compressed(f"{path}.bin", double_array)
#
#
# def import_binary_MDoubleArray(
#     name: str,
#     path: str = None,
#     compressed: bool = False
# ) -> om.MDoubleArray:
#
#     """
#     Importe un fichier MDoubleArray depuis un fichier binaire
#
#     Args:
#         name (str):
#             nom du fichier
#
#         path (str, optional):
#             chemin du fichier. Defaults to None.
#
#         compressed (bool, optional):
#             si True, le fichier est compressé.
#             Defaults to False.
#
#     Returns:
#         om.MDoubleArray
#             La liste importée
#     """
#
#     if not compressed:
#         path = (
#             f"{path}/{name}.bin"
#             if path
#             else f"{name}.bin"
#         )
#
#         double_array = np.fromfile(path, dtype=np.float64)
#
#     else:
#         path = (
#             f"{path}/{name}.bin.npz"
#             if path
#             else f"{name}.bin.npz"
#         )
#
#         double_array = np.load(path)["arr_0"]
#
#     return om.MDoubleArray(double_array)
#
#
# def import_binary_MIntArray(
#     name: str,
#     path: str = None,
#     compressed: bool = False
# ) -> om.MIntArray:
#
#     """
#     Importe un fichier MIntArray depuis un fichier binaire
#
#     Args:
#         name (str):
#             nom du fichier
#
#         path (str, optional):
#             chemin du fichier. Defaults to None.
#
#         compressed (bool, optional):
#             si True, le fichier est compressé.
#             Defaults to False.
#
#     Returns:
#         om.MIntArray
#             La liste importée
#     """
#
#     if not compressed:
#         path = (
#             f"{path}/{name}.bin"
#             if path
#             else f"{name}.bin"
#         )
#
#         int_array = np.fromfile(path, dtype=np.float64)
#
#     else:
#         path = (
#             f"{path}/{name}.bin.npz"
#             if path
#             else f"{name}.bin.npz"
#         )
#
#         int_array = np.load(path)["arr_0"]
#
#     return om.MIntArray(int_array)
