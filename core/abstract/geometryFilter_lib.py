from typing import Optional, Union, List, Set, Type

from maya.api import OpenMaya as om, OpenMayaAnim as oma

from . import dg_lib


class GeometryFilter(dg_lib.DGNode):

    def __init__(self, name: Union[str, om.MObject] = None) -> None:
        """
        Initialize an instance of GeometryFilter

        Args:
            name: Optional[str], the name of the node
        """

        super().__init__(name=name)

#     def printClass(
#         self
#     ) -> str:
#
#         """
#         Représentation de l'instance de la classe GeometryFilter.
#
#         Returns
#             str:
#                 Représentation de l'instance de la classe GeometryFilter.
#         """
#
#         txt = super().printClass()
#         txt += "\n"
#         txt += "\n# ######################################"
#         txt += "\n# - GEOMETRYFILTER PROPERTIES :"
#         txt += "\n# ######################################"
#         txt += "\n"
#         txt += f"\n - envelope                : bool : {self.envelope}"
#         txt += "\n"
#         txt += "\n - geometryFilter_fn       : oma.MFnGeometryFilter"
#         txt += "\n"
#         txt += (
#             "\n - input_geometries         : Optional[om.MObjectArray] : "
#             f"{self.input_geometries}"
#         )
#         txt += (
#             "\n - output_geometries        : Optional[om.MObjectArray] : "
#             f"{self.output_geometries}"
#         )
#         txt += "\n"
#         txt += (
#             "\n - input_geometries_names   : Optional[List[str]] : "
#             f"{self.input_geometries_names}"
#         )
#         txt += (
#             "\n - output_geometries_names  : Optional[List[str]] : "
#             f"{self.output_geometries_names}"
#         )
#         txt += "\n"
#         txt += (
#             "\n - input_geometry_types    :"
#             " [(apiType, apiTypeStr)] : "
#             f" {self.input_geometry_types}"
#         )
#         txt += (
#             "\n - output_geometry_mtypes  :"
#             " [(apiType, apiTypeStr)] : "
#             f" {self.output_geometry_types}"
#         )
#         txt += "\n"
#
#         return txt
#
# # - PROPERTIES ----------------------------------------------------------------
# # -----------------------------------------------------------------------------
# # - api OpenMayaAnim ----------------------------------------------------------
# # -----------------------------------------------------------------------------
#     @property
#     def geometryFilter_fn(
#         self
#     ) -> Optional[oma.MFnGeometryFilter]:
#
#         """
#         Renvoie l'objet MFnGeometryFilter de l'instance courante.
#
#         Returns:
#             Optional[om.MFnGeometryFilter]
#         """
#
#         return self._geometryFilter_fn
#
# # - Attributes ----------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     @property
#     def envelope(
#         self
#     ) -> bool:
#
#         """
#         Renvoie l'attribut envelope du deformer.
#
#         Returns:
#             bool
#         """
#
#         return (
#             self._get_envelope()
#             if self.exists
#             else self._envelope
#         )
#
#     @envelope.setter
#     def envelope(
#         self,
#         value: bool
#     ) -> None:
#
#         """
#         Définit l'attribut envelope du deformer.
#
#         Args:
#             value (bool):
#                 La valeur de l'attribut envelope du deformer.
#
#         Returns:
#             None
#         """
#
#         if self.exists:
#             self.plugs.set_bool("envelope", value)
#
#         self._envelope = value
#
# # - Geometries ----------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     @property
#     def input_geometries(
#         self
#     ) -> Optional[om.MObjectArray]:
#
#         """
#         Renvoie la liste des géométries d'entrée du deformer.
#
#         Returns:
#             Optional[om.MObjectArray]
#                 La liste des géométries d'entrée du deformer,
#                 ou None si le deformer n'existe pas.
#         """
#
#         return (
#             self.geometryFilter_fn.getInputGeometry()
#             if self.exists
#             else self._input_geometries
#         )
#
#     @input_geometries.setter
#     def input_geometries(
#         self,
#         geometries: Union[
#             om.MObjectArray,
#             List[om.MObject],
#             List[Type[dag_lib.DAGNode]],
#             List[str],
#             om.MObject,
#             Type[dag_lib.DAGNode],
#             str
#         ]
#     ) -> None:
#
#         """
#         Définit la liste des géométries d'entrée du deformer.
#
#         Args:
#             geometries (Union[
#                 om.MObjectArray,
#                 List[om.MObject],
#                 List[Type[dag_lib.DAGNode]],
#                 List[str],
#                 om.MObject,
#                 Type[dag_lib.DAGNode],
#                 str
#             ]):
#                 La liste des géométries d'entrée du deformer.
#
#         Returns:
#             None
#         """
#
#         self._input_geometries = convert.geometries_to_mObjectArray(
#             geometries
#         )
#
#         if self.exists:
#             self._disconnect_input_geometries()
#             self._add_input_geometries(self._input_geometries)
#
#     @property
#     def input_geometries_names(
#         self
#     ) -> Optional[List[str]]:
#
#         """
#         Renvoie la liste des noms des géométries d'entrée du deformer.
#
#         Returns:
#             Optional[List[str]]
#                 La liste des noms des géométries d'entrée du deformer,
#                 ou None si le deformer n'existe pas.
#         """
#
#         return [
#             om.MFnDependencyNode(input_geometry).name()
#             for input_geometry in self.input_geometries
#         ] if self.has_input_geometries else None
#
#     @property
#     def has_input_geometries(
#         self
#     ) -> bool:
#
#         """
#         Renvoie True si le deformer a des géométries d'entrée.
#
#         Returns:
#             bool
#         """
#
#         return bool(self.input_geometries)
#
#     @property
#     def output_geometries(
#         self
#     ) -> Optional[om.MObjectArray]:
#
#         """
#         Renvoie la liste des géométries de sortie du deformer.
#
#         Returns:
#             Optional[om.MObjectArray]
#                 La liste des géométries de sortie du deformer,
#                 ou None si le deformer n'existe pas.
#         """
#
#         return (
#             self.geometryFilter_fn.getOutputGeometry()
#             if self.exists
#             else self._output_geometries
#         )
#
#     @output_geometries.setter
#     def output_geometries(
#         self,
#         geometries: Union[
#             om.MObjectArray,
#             List[om.MObject],
#             List[Type[dag_lib.DAGNode]],
#             List[str],
#             om.MObject,
#             Type[dag_lib.DAGNode],
#             str
#         ]
#     ) -> None:
#
#         """
#         Définit la liste des géométries de sortie du deformer.
#
#         Args:
#             geometries (Union[
#                 om.MObjectArray,
#                 List[om.MObject],
#                 List[Type[dg_lib.DGNode]],
#                 List[str],
#                 om.MObject,
#                 Type[dg_lib.DGNode],
#                 str
#             ]):
#                 La liste des géométries de sortie du deformer.
#
#         Returns:
#             None
#         """
#
#         self._output_geometries = convert.geometries_to_mObjectArray(
#             geometries
#         )
#
#         if self.exists:
#             self._disconnect_output_geometries()
#             self._add_output_geometries(self._output_geometries)
#
#     @property
#     def output_geometries_names(
#         self
#     ) -> Optional[List[str]]:
#
#         """
#         Renvoie la liste des noms des géométries de sortie du deformer.
#
#         Returns:
#             Optional[List[str]]
#                 La liste des noms des géométries de sortie du deformer,
#                 ou None si le deformer n'existe pas.
#         """
#
#         return [
#             om.MFnDependencyNode(output_geometry).name()
#             for output_geometry in self.output_geometries
#         ] if self.has_output_geometries else None
#
#     @property
#     def has_output_geometries(
#         self
#     ) -> bool:
#
#         """
#         Renvoie True si le deformer a des géométries de sortie.
#
#         Returns:
#             bool
#         """
#
#         return bool(self.output_geometries)
#
#     @property
#     def input_geometry_types(
#         self
#     ) -> Optional[List[Set[Union[int, str]]]]:
#
#         """
#         Renvoie la liste des types de géométries d'entrée du deformer.
#
#         Returns:
#
#             Optional[List[Set[Union[int, str]]]]
#                 La liste des types de géométries d'entrée du deformer,
#                 ou None si le deformer n'existe pas.
#
#                 Exemple:
#                 [(294, "kNurbsSurface"), (296, "kmesh")]
#         """
#
#         return [
#             (input_geometry.apiType(), input_geometry.apiTypeStr)
#             for input_geometry in self.input_geometries
#         ] if self.has_input_geometries else None
#
#     @property
#     def output_geometry_types(
#         self
#     ) -> Optional[List[Set[Union[int, str]]]]:
#
#         """
#         Renvoie la liste des types de géométries de sortie du deformer.
#
#         Returns:
#             Optional[List[Set[Union[int, str]]]]
#
#                 La liste des types de géométries de sortie du deformer,
#                 ou None si le deformer n'existe pas.
#
#                 Exemple:
#                 [(294, "kNurbsSurface"), (296, "kmesh")]
#         """
#
#         return [
#             (output_geometry.apiType(), output_geometry.apiTypeStr)
#             for output_geometry in self.output_geometries
#         ] if self.has_output_geometries else None
#
# # - PUBLIC METHODS ------------------------------------------------------------
# # -----------------------------------------------------------------------------
# #     def create(
# #         self
# #     ) -> None:
# #
# #         """
# #         Crée le deformer, puis initialise la classe MFnGeometryFilter.
# #
# #         Args:
# #             incoming_connections (Optional[Dict[str, List[str]]]):
# #                 Un dictionnaire contenant pour clé le nom de l'attribut sortant
# #                 et pour valeur une liste de connections entrantes.
# #
# #             outgoing_connections (Optional[Dict[str, List[str]]]):
# #                 Un dictionnaire contenant pour clé le nom de l'attribut entrant
# #                 et pour valeur une liste de connections sortantes.
# #
# #         Returns:
# #             None
# #         """
# #
# #         for output_geometry in self.output_geometries:
# #
# #             cls_type = (
# #                 Mesh
# #                 if output_geometry.apiType() == Mesh.API_TYPE
# #                 else Surface if output_geometry.apiType() == Surface.API_TYPE
# #                 else Curve if output_geometry.apiType() == Curve.API_TYPE
# #                 else None
# #             )
# #
# #             shape_orig = cls_type(
# #                 om.MFnDagNode().setObject(
# #                     output_geometry).partialPathName()
# #             ).shape_orig
# #
# #             if not shape_orig.exists:
# #                 shape_orig.create()
# #
# #         super().create()
# #         self._geometryFilter_fn = oma.MFnGeometryFilter(self.maya_object)
#
# # - PRIVATE METHODS -----------------------------------------------------------
# # -----------------------------------------------------------------------------
# # - Class Init ----------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def _init_geometryFilter_attributes(
#         self
#     ) -> None:
#
#         """
#         Initialise les attributs du deformer.
#
#         Returns:
#             None
#         """
#
#         self._init_geometryFilter_fn()
#         self._envelope = self._get_envelope()
#
# # - api OpenMayaAnim ----------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def _init_geometryFilter_fn(
#         self
#     ) -> None:
#
#         """
#         Initialise l'objet MFnGeometryFilter de l'instance courante.
#
#         Returns:
#             None
#         """
#
#         self._geometryFilter_fn = (
#             oma.MFnGeometryFilter(self.maya_object)
#             if self.exists
#             else None
#         )
#
#         self._input_geometries = (
#             self.geometryFilter_fn.getInputGeometry()
#             if self.exists
#             else om.MObjectArray()
#         )
#
#         self._output_geometries = (
#             self.geometryFilter_fn.getOutputGeometry()
#             if self.exists
#             else om.MObjectArray()
#         )
#
# # - Envelope ------------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def _get_envelope(
#         self
#     ) -> float:
#
#         """
#         Renvoie la valeur de l'attribut envelope du deformer.
#
#         Returns:
#             float
#         """
#
#         if self.exists:
#
#             return self.plugs.get_plug("envelope").asFloat()
#
#         return (
#             self._envelope
#             if hasattr(self, "_envelope")
#             else 1.0
#         )
#
# # - Input Geometries ----------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def _add_input_geometries(
#         self,
#         geometries: Union[
#             List[om.MObject],
#             om.MObjectArray
#         ]
#     ) -> None:
#
#         """
#         Connecte les géométries d'entrée au deformer.
#
#         Args:
#             geometries (Union[List[om.MObject], om.MObjectArray]):
#                 La liste des géométries d'entrée du deformer.
#
#         Returns:
#             None
#         """
#
#         for i, geometry in enumerate(geometries):
#             self._add_input_geometry(
#                 geometry,
#                 i
#             )
#
#     def _add_input_geometry(
#         self,
#         geometry: om.MObject,
#         index: int
#     ) -> None:
#
#         """
#         Ajoute une géométrie d'entrée au deformer.
#
#         Args:
#             geometry (om.MObject):
#                 L'objet MObject de la géométrie.
#
#             index (int):
#                 L'index de connexion de la géométrie.
#
#         Returns:
#             None
#         """
#
#         orig_geo_plug = self.plugs.get_plug(f"originalGeometry[{index}]")
#         input_geo_plug = self.plugs.get_plug("inputGeometry")
#
#         if orig_geo_plug.isDestination:
#             self.disconnect_attr(
#                 orig_geo_plug.source(),
#                 orig_geo_plug
#             )
#
#         if input_geo_plug.isDestination:
#             self.disconnect_attr(
#                 input_geo_plug.source(),
#                 input_geo_plug
#             )
#
#         geo_name = om.MFnDependencyNode(geometry).name()
#
#         if geometry.apiType() == om.MFn.kMesh:
#             plug_src = dg_lib.DGNode(geo_name).plugs.get_plug("outMesh")
#             plug_src2 = dg_lib.DGNode(geo_name).plugs.get_plug("worldMesh[0]")
#         elif (
#             geometry.apiType() == om.MFn.kNurbsSurface
#             or geometry.apiType() == om.MFn.kNurbsCurve
#         ):
#             plug_src = dg_lib.DGNode(geo_name).plugs.get_plug("local")
#             plug_src2 = dg_lib.DGNode(geo_name).plugs.get_plug("worldSpace[0]")
#
#         self.connect_attr(plug_src, orig_geo_plug)
#         self.connect_attr(plug_src2, input_geo_plug)
#
#     def _disconnect_input_geometries(
#         self
#     ) -> None:
#
#         """
#         Déconnecte les géométries d'entrée du deformer.
#
#         Returns:
#             None
#         """
#
#         def_attr_names = [
#             attr_name
#             for attr_name in self.incoming_connections
#             if attr_name.startswith(f"{self.name}.originalGeometry")
#         ]
#
#         def_attr_names.extend([
#             attr_name
#             for attr_name in self.incoming_connections
#             if attr_name.startswith(f"{self.name}.inputGeometry")
#         ])
#
#         if def_attr_names:
#
#             self.disconnect_attrs(
#                 {
#                     def_attr_name: self.incoming_connections[def_attr_name]
#                     for def_attr_name in def_attr_names
#                 },
#                 None
#             )
#
# # - Output Geometries ---------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def _add_output_geometries(
#         self,
#         geometries: Union[
#             List[om.MObject],
#             om.MObjectArray
#         ]
#     ) -> None:
#
#         """
#         Connecte les géométries de sortie au deformer.
#
#         Args:
#             geometries (Union[List[om.MObject], om.MObjectArray]):
#                 La liste des géométries de sortie du deformer.
#
#         Returns:
#             None
#         """
#
#         for i, geometry in enumerate(geometries):
#
#             self._add_output_geometry(
#                 geometry,
#                 i
#             )
#
#     def _add_output_geometry(
#         self,
#         geometry: om.MObject,
#         index: int
#     ) -> None:
#
#         """
#         Ajoute une géométrie de sortie au deformer.
#
#         Args:
#             geometry (om.MObject):
#                 L'objet MObject de la géométrie.
#
#             index (int):
#                 L'index de connexion de la géométrie.
#
#         Returns:
#             None
#         """
#
#         attr = self.plugs.get_plug(f"outputGeometry[{index}]")
#
#         if attr.isSource:
#             for dest in attr.destinations():
#                 self.disconnect_attr(
#                     attr,
#                     dest
#                 )
#
#         geo_name = om.MFnDependencyNode(geometry).name()
#
#         if geometry.apiType() == om.MFn.kMesh:
#             plug_dest = dg_lib.DGNode(geo_name).plugs.get_plug("inMesh")
#         elif (
#             geometry.apiType() == om.MFn.kNurbsSurface
#             or geometry.apiType() == om.MFn.kNurbsCurve
#         ):
#             plug_dest = dg_lib.DGNode(geo_name).plugs.get_plug("create")
#
#         self.connect_attr(attr, plug_dest)
#
#     def _disconnect_output_geometries(
#         self
#     ) -> None:
#
#         """
#         Déconnecte les géométries de sortie du deformer.
#
#         Returns:
#             None
#         """
#
#         def_attr_names = [
#             attr_name
#             for attr_name in self.outgoing_connections
#             if attr_name.startswith(f"{self.name}.outputGeometry")
#         ]
#
#         if def_attr_names:
#
#             self.disconnect_attrs(
#                 None,
#                 {
#                     def_attr_name: self.incoming_connections[def_attr_name]
#                     for def_attr_name in def_attr_names
#                 }
#             )
#
# # - Geometries ----------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def _geometry_type(
#         self,
#         geometry: om.MObject
#     ) -> int:
#
#         """
#         Renvoie le type de la géométrie.
#
#         Args:
#             geometry (om.MObject):
#                 L'objet MObject de la géométrie.
#
#         Returns:
#             int:
#                 - 0 si la géométrie est un mesh.
#                 - 1 si la géométrie est une nurbsSurface.
#                 - 2 si la géométrie est une nurbsCurve.
#         """
#
#         if geometry.apiType() == om.MFn.kMesh:
#             return 0
#
#         elif geometry.apiType() == om.MFn.kNurbsSurface:
#             return 1
#
#         elif geometry.apiType() == om.MFn.kNurbsCurve:
#             return 2
#
#         else:
#
#             raise RuntimeError(
#                 "Error while getting geometry type."
#                 f"\n - geometry type: {geometry.apiTypeStr}"
#                 "\n - is not supported."
#             )
#
#     def _get_component_count(
#         self,
#         geometry: om.MObject
#     ) -> Optional[int]:
#
#         """
#         Renvoie le nombre de composants de la géométrie.
#
#         Args:
#             geometry (om.MObject):
#                 L'objet MObject de la géométrie.
#
#         Returns:
#             Optional[int]:
#                 Le nombre de composants de la géométrie,
#                 ou None si la géométrie n'est pas supportée.
#         """
#
#         if geometry.isNull():
#
#             return 0
#
#         elif geometry.apiType() == om.MFn.kMesh:
#
#             mfnGeo = om.MFnMesh(geometry)
#
#             return (
#                 idx
#                 if (idx := mfnGeo.numVertices) is not None
#                 else 0
#             )
#
#         elif geometry.apiType() == om.MFn.kNurbsCurve:
#
#             mfnGeo = om.MFnNurbsCurve(geometry)
#
#             return (
#                 idx
#                 if (idx := mfnGeo.numCVs) is not None
#                 else 0
#             )
#
#         elif geometry.apiType() == om.MFn.kNurbsSurface:
#
#             mfnGeo = om.MFnNurbsSurface(geometry)
#
#             return (
#                 idx
#                 if (idx := mfnGeo.numCVsInU * mfnGeo.numCVsInV) is not None
#                 else 0
#             )
#
#         raise RuntimeError(
#             "Error while getting component count:"
#             f"\n - geometry type: {geometry.apiTypeStr}"
#             "\n - is not supported."
#         )
