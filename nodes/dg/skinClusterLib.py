from typing import Optional, Union, List, Dict, Set, Type

from maya import cmds
from maya.api import OpenMaya as om, OpenMayaAnim as oma

from ...core import NodeType, DAGType, DGType
from ...core.abstract import geometryFilterLib
from ...core.nodeRegistry import NodeRegistry
from ...core.graphLib import Graph


# TODO: Still some work to do here
class SkinCluster(geometryFilterLib.GeometryFilter):

    _NODE_TYPE = "skinCluster"
    _API_TYPE = om.MFn.kSkinClusterFilter

    @property
    def mfnSkinCluster(self) -> oma.MFnSkinCluster:
        """
        Get mfnSkinCluster of the om.MObject

        :return: oma.mfnSkinCluster, the skinCluster object
        """
        return oma.MFnSkinCluster(self)

    @property
    def bindPose(self) -> DGType:

        """
        Get the DagPose node connected to bindPose attr

        :return: DagPose, the DagPose node connected to bindPose attr
        """
        
        dagPoseNode = self['bindPose'].source().node()
        return Graph(dagPoseNode)[0] if dagPoseNode else None

    @property
    def influenceObjects(self) -> Graph:
        """
        Get an om.MSelectionList of all influence objects

        :return: om.MSelectionList, a list of influence objects
        """

        graph = Graph()
        for obj in self.mfnSkinCluster.influenceObjects():
            graph.add(obj.node())

        return graph

    @property
    def weights(self) -> Dict[DAGType, om.MDoubleArray]:

        """
        Get the list of current weights

        :return: Dict[DAGType, om.MDoubleArray],
            the list of current weights for each output mesh
        """
        weightDict = {}
        for deformedMesh in self.outputGeometry:
            vtxList = f'{deformedMesh.name}.vtx[*]'
            compMObj = om.MGlobal.getSelectionListByName(vtxList).getComponent(0)[1]
            meshDagPath = deformedMesh.dagPath
            weightDict[deformedMesh] = self.mfnSkinCluster.getWeights(meshDagPath, compMObj)

        return weightDict

    def getInfluencesFromVertex(self, vertexIdx: int) -> Dict[str, List[str]]:
        """
        Get influences affecting given vertex

        :param vertexIdx: int, the vertex index

        :return: Dict[str, List[str]], dict{'mesh.vtx[vtxIdx]': ['joint1', 'joint2']}
        """

        vertInfluenceDict = {}
        vertexName = f'{self.outputGeometry[0].name}.vtx[{vertexIdx}]'

        for influence in cmds.skinCluster(self.name, query=True, weightedInfluence=True):

            # maya is stupid and the only way to get vertices from an influence
            # is to select them
            cmds.skinCluster(self.name, edit=True, selectInfluenceVerts=influence)
            influencedVertices = cmds.ls(selection=True, flatten=True)

            if vertexName not in influencedVertices:
                continue

            vertInfluenceDict.setdefault(vertexName, []).append(influence)

        return vertInfluenceDict


#     @weights.setter
#     def weights(
#         self,
#         weights: Union[
#             om.MDoubleArray,
#             Dict[str, float],
#             List[Set[Union[str, float]]],
#             List[float]
#         ]
#     ) -> None:
#
#         """
#         Définit la liste des weights du node courant.
#
#         Args:
#             weights (Union[om.MDoubleArray, List[float]]):
#                 La liste des weights à définir.
#
#         Returns:
#             None
#         """
#
#         weights = self._check_weights(weights)
#
#         if self.exists:
#             self._set_weights(weights)
#
#         self._weights = weights
#
#     @property
#     def blend_weights(
#         self
#     ) -> om.MDoubleArray:
#
#         """
#         Renvoie la liste des blend weights du node courant.
#
#         Returns:
#             om.MDoubleArray
#                 La liste des blend weights du node courant.
#         """
#
#         return self._init_blend_weights()
#
#     @blend_weights.setter
#     def blend_weights(
#         self,
#         blend_weights: Union[
#             om.MDoubleArray,
#             Dict[str, float],
#             List[Set[Union[str, float]]],
#             List[float]
#         ]
#     ) -> None:
#
#         """
#         Définit la liste des blend weights du node courant.
#
#         Args:
#             blend_weights (Union[om.MDoubleArray, List[float]]):
#                 La liste des blend weights à définir.
#
#         Returns:
#             None
#         """
#
#         blend_weights = self._check_weights(blend_weights)
#
#         if self.exists:
#             self._set_blend_weights(blend_weights)
#
#         self._blend_weights = blend_weights
#
#     @property
#     def influence_objects(
#         self
#     ) -> om.MDagPathArray:
#
#         """
#         Renvoie la liste des influence objects du node courant.
#
#         Returns:
#             om.MDagPathArray
#         """
#
#         return (
#             self.skincluster_fn.influenceObjects()
#             if self.exists
#             and self.plugs.get_plug('matrix').numElements() > 0
#             else self._influence_objects
#         )
#
#     @influence_objects.setter
#     def influence_objects(
#         self,
#         influence_objects: Union[
#             om.MDagPathArray,
#             List[om.MDagPath],
#             List[Type[dagLib.DAGNode]],
#             List[str],
#             om.MDagPath,
#             Type[dagLib.DAGNode],
#             str
#         ]
#     ) -> None:
#
#         """
#         Définit la liste des influence objects du node courant.
#
#         Args:
#             influence_objects (
#                 Union[
#                     om.MDagPathArray,
#                     List[om.MDagPath],
#                     List[lib_nde.Node],
#                     List[str],
#                     om.MDagPath,
#                     lib_nde.Node,
#                     str
#                 ]
#             ):
#                 La liste des influence objects à définir.
#
#         Returns:
#             None
#         """
#
#         influence_objects = convert.geometries_to_mdagpath_array(
#             influence_objects
#         )
#         self._influence_objects = influence_objects
#
#         if not self.exists:
#             return
#
#         self._disconnect_influence_objects()
#         self._connect_influence_objects(influence_objects)
#
#     @influence_objects.deleter
#     def influence_objects(
#         self
#     ) -> None:
#
#         """
#         Supprime la liste des influence objects du node courant.
#
#         Returns:
#             None
#         """
#
#         self._disconnect_influence_objects()
#         self._influence_objects = om.MDagPathArray()
#
#     @property
#     def influence_names(
#         self
#     ) -> List[Optional[str]]:
#
#         """
#         Renvoie la liste des influence names du node courant.
#
#         Returns:
#             List[Optional[str]]
#         """
#
#         return [
#             x.partialPathName()
#             for x in self.influence_objects
#         ]
#
#     @property
#     def influences_len(
#         self
#     ) -> int:
#
#         """
#         Renvoie le nombre d'influences du node courant.
#
#         Returns:
#             int
#         """
#
#         return (
#             len(self.influence_objects)
#             if self.influence_objects is not None
#             else 0
#         )
#
# # - Components ----------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     @property
#     def skinned_components(
#         self
#     ) -> Optional[om.MSelectionList]:
#
#         """
#         Renvoie la liste des components skinnés du node courant.
#
#         Returns:
#             Optional[om.MSelectionList]
#                 La liste des components skinnés du node courant.
#         """
#
#         if not self.has_output_geometries:
#             return None
#
#         component_type_str = self._get_component_type_str(
#             self.output_geometry_types[0][0]
#         )
#
#         return (
#             om.MGlobal.getSelectionListByName(
#                 f"{self.output_geometries_names[0]}.{component_type_str}[*]"
#             ).getComponent(0)[1]
#         )
#
#     @property
#     def skinned_components_names(
#         self
#     ) -> Optional[List[str]]:
#
#         """
#         Renvoie la liste des noms des components skinnés du node courant.
#
#         Returns:
#             Optional[List[str]]
#                 La liste des noms des components skinnés du node courant.
#         """
#
#         if not self.has_output_geometries:
#             return None
#
#         component_type_str = self._get_component_type_str(
#             self.output_geometry_types[0][0]
#         )
#
#         return [
#             f"{self.output_geometries_names[0]}.{component_type_str}[{i}]"
#             for i in range(self.output_components_count)
#         ]
#
#     @property
#     def input_components_count(
#         self
#     ) -> int:
#
#         """
#         Renvoie le nombre de components d'entrée du node courant.
#
#         Returns:
#             int
#         """
#
#         return (
#             sum(
#                 self._get_component_count(self.input_geometries[i])
#                 for i in range(len(self.input_geometries))
#             ) if self.input_geometries else 0
#         )
#
#     @property
#     def output_components_count(
#         self
#     ):
#
#         """
#         Renvoie le nombre de components de sortie du node courant.
#
#         Returns:
#             int
#         """
#
#         return (
#             sum(
#                 self._get_component_count(self.output_geometries[i])
#                 for i in range(len(self.output_geometries))
#             ) if self.output_geometries else 0
#         )
#
#     @property
#     def use_components(
#         self
#     ) -> bool:
#
#         """
#         Renvoie si le node courant utilise des components.
#
#         Returns:
#             bool
#         """
#
#         return self._init_use_components()
#
#     @use_components.setter
#     def use_components(
#         self,
#         use_components: bool
#     ) -> None:
#
#         """
#         Définit si le node courant utilise des components.
#
#         Args:
#             use_components (bool):
#                 Si le node courant utilise des components.
#
#         Returns:
#             None
#         """
#
#         if self.exists:
#             self.set_bool_attr(
#                 "useComponents",
#                 use_components
#             )
#
#         self._use_components = use_components
#
# # - Skinning Method -----------------------------------------------------------
# # -----------------------------------------------------------------------------
#     @property
#     def skinning_method(
#         self
#     ) -> int:
#
#         """
#         Renvoie la méthode de skinning du node courant.
#
#         Returns:
#             int
#         """
#
#         return self._init_skinning_method()
#
#     @skinning_method.setter
#     def skinning_method(
#         self,
#         skinning_method: Union[int, str]
#     ) -> None:
#
#         """
#         Définit la méthode de skinning du node courant.
#
#         Args:
#             skinning_method (Union[int, str]):
#                 La méthode de skinning à définir.
#
#         Returns:
#             None
#         """
#
#         skinning_method = self._check_skinning_method(skinning_method)
#
#         if self.exists:
#             self.set_int_attr(
#                 "skinningMethod",
#                 skinning_method
#             )
#
#         self._skinning_method = skinning_method
#
# # - DQS -----------------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     @property
#     def dqs_support_nonRigid(
#         self
#     ) -> bool:
#
#         """
#         Renvoie si le node courant supporte le DQS non-rigide.
#
#         Returns:
#             bool
#         """
#
#         return self._init_dqs_support_nonRigid()
#
#     @dqs_support_nonRigid.setter
#     def dqs_support_nonRigid(
#         self,
#         dqs_support_nonRigid: bool
#     ) -> None:
#
#         """
#         Définit si le node courant supporte le DQS non-rigide.
#
#         Args:
#             dqs_support_nonRigid (bool):
#                 Si le node courant supporte le DQS non-rigide.
#
#         Returns:
#             None
#         """
#
#         if self.exists:
#             self.set_bool_attr(
#                 "dqsSupportNonRigid",
#                 dqs_support_nonRigid
#             )
#
#         self._dqs_support_nonRigid = dqs_support_nonRigid
#
#     @property
#     def dqs_scaleX(
#         self
#     ) -> float:
#
#         """
#         Renvoie la valeur de l'attribut 'dqsScaleX' du node courant.
#
#         Returns:
#             float
#         """
#
#         return self._get_dqs_scale_value("dqsScaleX")
#
#     @dqs_scaleX.setter
#     def dqs_scaleX(
#         self,
#         dqs_scaleX: Union[float, int]
#     ) -> None:
#
#         """
#         Définit la valeur de l'attribut 'dqsScaleX' du node courant.
#
#         Args:
#             dqs_scaleX (float):
#                 La valeur de l'attribut 'dqsScaleX' à définir.
#
#         Returns:
#             None
#         """
#
#         if isinstance(dqs_scaleX, int):
#             dqs_scaleX = float(dqs_scaleX)
#
#         if self.exists:
#             self.set_float_attr(
#                 "dqsScaleX",
#                 dqs_scaleX
#             )
#
#         self._dqs_scaleX = dqs_scaleX
#
#     @property
#     def dqs_scaleY(
#         self
#     ) -> float:
#
#         """
#         Renvoie la valeur de l'attribut 'dqsScaleY' du node courant.
#
#         Returns:
#             float
#         """
#
#         return self._get_dqs_scale_value("dqsScaleY")
#
#     @dqs_scaleY.setter
#     def dqs_scaleY(
#         self,
#         dqs_scaleY: Union[float, int]
#     ) -> None:
#
#         """
#         Définit la valeur de l'attribut 'dqsScaleY' du node courant.
#
#         Args:
#             dqs_scaleY (float):
#                 La valeur de l'attribut 'dqsScaleY' à définir.
#
#         Returns:
#             None
#         """
#
#         if isinstance(dqs_scaleY, int):
#             dqs_scaleY = float(dqs_scaleY)
#
#         if self.exists:
#             self.set_float_attr(
#                 "dqsScaleY",
#                 dqs_scaleY
#             )
#
#         self._dqs_scaleY = dqs_scaleY
#
#     @property
#     def dqs_scaleZ(
#         self
#     ) -> float:
#
#         """
#         Renvoie la valeur de l'attribut 'dqsScaleZ' du node courant.
#
#         Returns:
#             float
#         """
#
#         return self._get_dqs_scale_value("dqsScaleZ")
#
#     @dqs_scaleZ.setter
#     def dqs_scaleZ(
#         self,
#         dqs_scaleZ: Union[float, int]
#     ) -> None:
#
#         """
#         Définit la valeur de l'attribut 'dqsScaleZ' du node courant.
#
#         Args:
#             dqs_scaleZ (float):
#                 La valeur de l'attribut 'dqsScaleZ' à définir.
#
#         Returns:
#             None
#         """
#
#         if isinstance(dqs_scaleZ, int):
#             dqs_scaleZ = float(dqs_scaleZ)
#
#         if self.exists:
#             self.set_float_attr(
#                 "dqsScaleZ",
#                 dqs_scaleZ
#             )
#
#         self._dqs_scaleZ = dqs_scaleZ
#
# # - Attributes ----------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     @property
#     def deform_user_normals(
#         self
#     ) -> bool:
#
#         """
#         Renvoie si le node courant déforme les user normals.
#
#         Returns:
#             bool
#         """
#
#         return self._init_deform_user_normals()
#
#     @deform_user_normals.setter
#     def deform_user_normals(
#         self,
#         deform_user_normals: bool
#     ) -> None:
#
#         """
#         Définit si le node courant déforme les user normals.
#
#         Args:
#             deform_user_normals (bool):
#                 Si le node courant déforme les user normals.
#
#         Returns:
#             None
#         """
#
#         if self.exists:
#             self.set_bool_attr(
#                 "deformUserNormals",
#                 deform_user_normals
#             )
#
#         self._deform_user_normals = deform_user_normals
#
#     @property
#     def normalize_weights(
#         self
#     ) -> bool:
#
#         """
#         Renvoie si le node courant normalise les weights.
#
#         Returns:
#             bool
#         """
#
#         return self._init_normalize_weights()
#
#     @normalize_weights.setter
#     def normalize_weights(
#         self,
#         normalize_weights: bool
#     ) -> None:
#
#         """
#         Définit si le node courant normalise les weights.
#
#         Args:
#             normalize_weights (bool):
#                 Si le node courant normalise les weights.
#
#         Returns:
#             None
#         """
#
#         normalize_weights = self._check_normalize_weights(normalize_weights)
#
#         if self.exists:
#             self.set_bool_attr(
#                 "normalizeWeights",
#                 normalize_weights
#             )
#
#         self._normalize_weights = normalize_weights
#
#     @property
#     def weight_distribution(
#         self
#     ) -> int:
#
#         """
#         Renvoie la méthode de distribution des weights du node courant.
#
#         Returns:
#             int
#         """
#
#         return self._init_weight_distribution()
#
#     @weight_distribution.setter
#     def weight_distribution(
#         self,
#         weight_distribution: Union[int, str]
#     ) -> None:
#
#         """
#         Définit la méthode de distribution des weights du node courant.
#
#         Args:
#             weight_distribution (Union[int, str]):
#                 La méthode de distribution des weights à définir.
#
#         Returns:
#             None
#         """
#
#         weight_distribution = self._check_weight_distribution(
#             weight_distribution
#         )
#
#         if self.exists:
#             self.set_int_attr(
#                 "weightDistribution",
#                 weight_distribution
#             )
#
#         self._weight_distribution = weight_distribution
#
#     @property
#     def max_influences(
#         self
#     ) -> int:
#
#         """
#         Renvoie le nombre maximum d'influences du node courant.
#
#         Returns:
#             int
#         """
#
#         return self._init_max_influences()
#
#     @max_influences.setter
#     def max_influences(
#         self,
#         max_influences: int
#     ) -> None:
#
#         """
#         Définit le nombre maximum d'influences du node courant.
#
#         Args:
#             max_influences (int):
#                 Le nombre maximum d'influences à définir.
#
#         Returns:
#             None
#         """
#
#         if self.exists:
#             self.set_int_attr(
#                 "maxInfluences",
#                 max_influences
#             )
#
#         self._max_influences = max_influences
#
#     @property
#     def maintain_max_influences(
#         self
#     ) -> bool:
#
#         """
#         Renvoie si le node courant maintient le nombre maximum d'influences.
#
#         Returns:
#             bool
#         """
#
#         return self._init_maintain_max_influences()
#
#     @maintain_max_influences.setter
#     def maintain_max_influences(
#         self,
#         maintain_max_influences: bool
#     ) -> None:
#
#         """
#         Définit si le node courant maintient le nombre maximum d'influences.
#
#         Args:
#             maintain_max_influences (bool):
#                 Si le node courant maintient le nombre maximum d'influences.
#
#         Returns:
#             None
#         """
#
#         if self.exists:
#             self.set_bool_attr(
#                 "maintainMaxInfluences",
#                 maintain_max_influences
#             )
#
#         self._maintain_max_influences = maintain_max_influences
#
# # - PUBLIC METHODS ------------------------------------------------------------
# # -----------------------------------------------------------------------------
# # - Create/Delete/Update ------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def create(
#         self
#     ) -> None:
#
#         """
#         Crée le node Maya s'il n'existe pas déjà.
#
#         Returns:
#             None
#         """
#
#         super().create()
#
#         self._skincluster_fn = oma.MFnSkinCluster(self.maya_object)
#         self.bind_pose.create()
#         self.bind_pose.connect_attr(
#             f"{self.bind_pose.name}.message",
#             f"{self.name}.bindPose"
#         )
#         self.bind_pose.bind_pose = True
#         plugs = self.plugs
#
#         if self._output_geometries:
#             for i, output_geometry in enumerate(self._output_geometries):
#
#                 geo = dagLib.DAGNode(
#                     om.MFnDependencyNode(output_geometry).name()
#                 )
#                 geo_plugs = geo.plugs
#
#                 dest_plug = geo_plugs.get_plug((
#                     "create"
#                     if output_geometry.apiType() in [284, 267]
#                     else "inMesh"
#                 ))
#
#                 if dest_plug.isDestination:
#                     self.disconnect_attr(dest_plug.source(), dest_plug)
#
#                 self.connect_attr(
#                     plugs.get_plug(
#                         "outputGeometry").elementByLogicalIndex(i),
#                     dest_plug
#                 )
#
#                 orig_plugs = geo.shape_orig.plugs
#
#                 src_plug = orig_plugs.get_plug((
#                     "local"
#                     if output_geometry.apiType() in [284, 267]
#                     else "outMesh"
#                 ))
#
#                 self.connect_attr(
#                     src_plug,
#                     plugs.get_plug(
#                         "originalGeometry").elementByLogicalIndex(i)
#                 )
#
#                 src_plug = orig_plugs.get_plug((
#                     "worldSpace[0]"
#                     if output_geometry.apiType() in [284, 267]
#                     else "worldMesh[0]"
#                 ))
#
#                 self.connect_attr(
#                     src_plug,
#                     plugs.get_plug(
#                         "input").elementByLogicalIndex(i).child(0)
#                 )
#
#         if (
#             self.influence_objects is not None
#             and len(self.influence_objects) > 0
#         ):
#             self._connect_influence_objects(self.influence_objects)
#             self.weights = self._default_weights()
#
#         self._set_bind_pre_matrices()
#
#     # - Influence Objects ----------------------------------------------------
#     # -------------------------------------------------------------------------
#     def add_influence_objects(
#         self,
#         influence_objects: Union[
#             om.MDagPathArray,
#             List[om.MDagPath],
#             List[Type[dagLib.DAGNode]],
#             List[str],
#             om.MDagPath,
#             Type[dagLib.DAGNode],
#             str
#         ]
#     ) -> None:
#
#         """
#         Ajoute des influence objects au node courant.
#
#         Args:
#             influence_objects (
#                 Union[
#                     om.MDagPathArray,
#                     List[om.MDagPath],
#                     List[lib_nde.Node],
#                     List[str],
#                     om.MDagPath,
#                     lib_nde.Node,
#                     str
#                 ]
#             ):
#                 Les influence objects à ajouter.
#
#         Returns:
#             None
#         """
#
#         influence_objects = convert.geometries_to_mdagpath_array(
#             influence_objects
#         )
#
#         self.influence_objects = om.MDagPathArray(
#             self.influence_objects
#             + influence_objects
#         ) if self.influence_objects is not None else influence_objects
#
#     def remove_influence_objects(
#         self,
#         influence_objects: Union[
#             om.MDagPathArray,
#             List[om.MDagPath],
#             List[Type[dagLib.DAGNode]],
#             List[str],
#             om.MDagPath,
#             Type[dagLib.DAGNode],
#             str
#         ]
#     ) -> None:
#
#         """
#         Supprime des influence objects du node courant.
#
#         Args:
#             influence_objects (
#                 Union[
#                     om.MDagPathArray,
#                     List[om.MDagPath],
#                     List[lib_nde.Node],
#                     List[str],
#                     om.MDagPath,
#                     lib_nde.Node,
#                     str
#                 ]
#             ):
#                 Les influence objects à supprimer.
#
#         Returns:
#             None
#         """
#
#         bind_pose = self.bind_pose
#         bind_plugs = bind_pose.plugs
#         plugs = self.plugs
#         attrs = [
#             "matrix",
#             "influenceColor",
#             "lockWeights"
#         ]
#         bind_attrs = [
#             'members',
#             'worldMatrix'
#         ]
#
#         influence_objects = convert.geometries_to_mdagpath_array(
#             influence_objects
#         )
#
#         indices = []
#
#         for i, obj in enumerate(self.influence_objects):
#             if obj in influence_objects:
#                 indices.append(i)
#
#         for index in indices[::-1]:
#             for attr in attrs:
#                 plug = plugs.get_plug(attr).elementByPhysicalIndex(index)
#                 self.disconnect_attr(plug.source(), plug)
#
#         influence_objects = om.MObjectArray([
#             dagPath.node()
#             for dagPath in influence_objects
#         ])
#
#         members = om.MObjectArray([
#             plug.source().node()
#             for plug in bind_pose.members
#         ])
#
#         indices = []
#
#         for i, obj in enumerate(members):
#             if obj in influence_objects:
#                 indices.append(i)
#
#         for index in indices[::-1]:
#             for attr in bind_attrs:
#
#                 plug = bind_plugs.get_plug(attr).elementByPhysicalIndex(index)
#
#                 if not plug.isDestination:
#                     continue
#
#                 self.disconnect_attr(plug.source(), plug)
#
#     def get_components_from_influence(
#         self,
#         influence_name: str
#     ) -> list[str]:
#
#         """
#         Gets a list of vertices affected by the given transform
#         :param influence_name: the name of the influence object
#         :return: a list of vertices
#         """
#
#         # TODO: refactor to OpenMaya function
#         if influence_name not in mc.skinCluster(self.name, q=True, inf=True):
#             mc.warning(
#                 "Influence object is not"
#                 f" part of the SkinCluster : {influence_name}"
#             )
#             return []
#
#         temp_selection_buffer = mc.ls(sl=True)
#         mc.select(None)
#
#         mc.skinCluster(self.name, e=True, siv=influence_name)
#         verts = mc.ls(sl=True, fl=True)
#
#         mc.select(temp_selection_buffer)
#
#         return verts
#
#     def get_component_influence_data(self) -> dict['str': list['str']]:
#         """
#         Dictionary of influence/influenced_components pairs
#         :return: a dictionary with influence/influenced_components pairs
#         """
#         inf_dict = {}
#         for influence in mc.skinCluster(self.name, q=True, inf=True):
#             inf_dict[influence] = self.get_components_from_influence(influence)
#
#         return inf_dict
#
#     # - SkinCluster Data ------------------------------------------------------
#     # -------------------------------------------------------------------------
#     def dict_data(
#         self
#     ):
#
#         return {
#             "input_geometries": [
#                 input_geo.fullPathName()
#                 for input_geo in self.input_geometries
#             ],
#             "output_geometries": [
#                 output_geo.fullPathName()
#                 for output_geo in self.output_geometries
#             ],
#             "input_geometry_MTypes": [
#                 input_geometry_type[0]
#                 for input_geometry_type in self.input_geometry_types
#             ],
#             "input_geometry_type_str": [
#                 input_geometry_type[1]
#                 for input_geometry_type in self.input_geometry_types
#             ],
#             "output_components_count": self.output_components_count,
#             "influences_len": self.influences_len,
#             "skinning_method": self.skinning_method,
#             "use_components": self.use_components,
#             "deform_user_normals": self.deform_user_normals,
#             "dqs_support_nonRigid": self.dqs_support_nonRigid,
#             "dqs_scaleX": self.dqs_scaleX,
#             "dqs_scaleY": self.dqs_scaleY,
#             "dqs_scaleZ": self.dqs_scaleZ,
#             "normalize_weights": self.normalize_weights,
#             "weight_distribution": self.weight_distribution,
#             "max_influences": self.max_influences,
#             "maintain_max_influences": self.maintain_max_influences,
#             "blend_weights": self.blend_weights
#         }
#
# # - PRIVATE METHODS -----------------------------------------------------------
# # -----------------------------------------------------------------------------
# # - Properties ----------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def _init_skincluster_properties(
#         self,
#         influence_objects: Optional[Union[
#             om.MDagPathArray,
#             List[om.MDagPath],
#             List[Type[dagLib.DAGNode]],
#             List[str],
#             om.MDagPath,
#             Type[dagLib.DAGNode],
#             str
#         ]] = None
#     ) -> None:
#
#         """
#         Initialise les variables privées appelées dans les properties de
#         l'instance courante.
#
#         Args:
#             influence_objects (Optional[
#                 Union[
#                     om.MDagPathArray,
#                     List[om.MDagPath],
#                     List[Type[dagLib.DAGNode]],
#                     List[str],
#                     om.MDagPath,
#                     Type[dagLib.DAGNode],
#                     str
#                 ]
#             ]):
#                 Les influence objects à initialiser.
#
#         Returns:
#             None
#         """
#
#         self._init_skincluster_fn()
#         self._init_bind_pose()
#         self._init_influence_objects(influence_objects)
#
# # - Bind Pose -----------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def _init_bind_pose(
#         self
#     ) -> None:
#
#         """
#         Initialise la variable privée '_bind_pose' de l'instance courante.
#
#         Returns:
#             None
#         """
#
#         if self.exists:
#             _bind_pose = self._get_bind_pose()
#             if _bind_pose is not None:
#                 self._bind_pose = _bind_pose
#                 return
#
#         name = (
#             self.name.replace("skinCluster", "bindPose")
#             if "skinCluster" in self.name
#             else f"{self.name}_bindPose"
#         )
#         self._bind_pose = DagPose(name)
#
#     def _get_bind_pose(
#         self
#     ) -> Optional[DagPose]:
#
#         """
#         Renvoie la bind pose du node courant.
#
#         Returns:
#             Optional[DagPose]
#                 La bind pose du node courant.
#         """
#
#         bind_pose_plug = self.plugs.get_plug("bindPose")
#
#         if bind_pose_plug.isConnected:
#             return DagPose(
#                 om.MFnDependencyNode(
#                     bind_pose_plug.source().node()
#                 ).name()
#             )
#
#         return None
#
# # - Bind Pre Matrix -----------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def _set_bind_pre_matrices(
#         self
#     ) -> None:
#
#         """
#         Définit les bind pre matrices du node courant.
#
#         Returns:
#             None
#         """
#
#         bpm_plug = self.plugs.get_plug("bindPreMatrix")
#
#         for i in range(self.influences_len):
#             inv_mtx_plug = dagLib.DAGNode(
#                 self.influence_names[i]
#             ).plugs.get_plug("worldInverseMatrix")
#
#             mtx = inv_mtx_plug.elementByLogicalIndex(
#                 0).asMObject()
#
#             bpm_plug.elementByLogicalIndex(
#                 i).setMObject(
#                     mtx)
#
# # - Weights -------------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def _init_weights(
#         self
#     ) -> None:
#
#         """
#         Initialise la variable privée '_weights' de l'instance courante.
#
#         Si le node courant n'existe pas, la variable privée '_weights'
#         est initialisée à une liste vide. Sinon, la variable privée
#         '_weights' est initialisée à la liste des weights du node
#         courant.
#
#         Returns:
#             None
#         """
#
#         return (
#             self.skincluster_fn.getWeights(
#                 dagLib.DAGNode(self.output_geometries_names[0]).maya_dagPath,
#                 self.skinned_components
#             )[0]
#             if self.exists
#             and self.has_output_geometries
#             else (
#                 (
#                         self._weights
#                         if self._weights is not None
#                         and hasattr(self, "_weights")
#                         else self._default_weights()
#                 )
#             )
#         )
#
#     def _init_blend_weights(
#         self
#     ) -> om.MDoubleArray:
#
#         """
#         Initialise la variable privée '_blend_weights' de l'instance courante.
#
#         Si le node courant n'existe pas, la variable privée '_blend_weights'
#         est initialisée à une liste vide. Sinon, la variable privée
#         '_blend_weights' est initialisée à la liste des blend weights du node
#         courant.
#
#         Returns:
#             None
#         """
#         if self.exists and self.has_output_geometries:
#             blend_weights = self.skincluster_fn.getBlendWeights(
#                 dagLib.DAGNode(self.output_geometries_names[0]).maya_dagPath,
#                 self.skinned_components
#             )
#         elif (hasattr(self, "_blend_weights") and
#               self._blend_weights is not None):
#             blend_weights = self._blend_weights
#         else:
#             blend_weights = om.MDoubleArray()
#
#         return blend_weights
#
#     def _check_weights(
#         self,
#         weights: Union[
#             om.MDoubleArray,
#             Dict[str, float],
#             List[Set[Union[str, float]]],
#             List[float]
#         ]
#     ) -> om.MDoubleArray:
#
#         """
#         Vérifie si la liste des weights spécifiée est valide.
#
#         Args:
#             blend_weights (Union[
#                 om.MDoubleArray,
#                 Dict[str, float],
#                 List[Set[str, float]],
#                 List[float]
#             ]):
#                 La liste des blend weights à vérifier.
#
#         Raises:
#             ValueError:
#                 Si la liste des blend weights spécifiée est invalide.
#
#         Returns:
#             om.MDoubleArray
#                 La liste des blend weights.
#         """
#
#         if len(weights) != self.input_components_count*self.influences_len:
#
#             raise ValueError(
#                 "Error while setting weights:"
#                 "\n - Invalid blend weights count:"
#                 f"\n - ({len(weights)} != "
#                 f"{self.output_components_count*self.influences_len})"
#             )
#
#         if (
#             isinstance(weights, list)
#             and all(isinstance(x, float) for x in weights)
#         ):
#
#             return om.MDoubleArray(weights)
#
#         elif (
#             isinstance(weights, list)
#             and all(isinstance(x, set) for x in weights)
#             and all(
#                 isinstance(x[0], str)
#                 and isinstance(x[1], float)
#                 for x in weights
#             )
#         ):
#
#             return om.MDoubleArray(
#                 [
#                     x[1]
#                     for x in weights
#                 ]
#             )
#
#         elif (
#             isinstance(weights, dict)
#             and all(isinstance(x, str) for x in weights.keys())
#             and all(isinstance(x, float) for x in weights.values())
#         ):
#
#             return om.MDoubleArray(
#                 [
#                     weights[x]
#                     for x in weights.keys()
#                 ]
#             )
#
#         elif isinstance(weights, om.MDoubleArray):
#
#             return weights
#
#         else:
#
#             raise ValueError(
#                 "Error while setting weights:"
#                 "\n - Invalid weights type:"
#                 f"\n - {type(weights)}"
#             )
#
#     def _set_weights(
#         self,
#         weights: om.MDoubleArray
#     ) -> None:
#
#         """
#         Définit la liste des weights du node courant.
#
#         Args:
#             weights (om.MDoubleArray):
#                 La liste des weights à définir.
#
#         Returns:
#             None
#         """
#
#         self.skincluster_fn.setWeights(
#             dagLib.DAGNode(self.output_geometries_names[0]).maya_dagPath,
#             self.skinned_components,
#             om.MIntArray(list(range(self.influences_len))),
#             weights,
#             True,
#             False,
#         )
#
#     def _init_normalize_weights(
#         self
#     ) -> bool:
#
#         """
#         Initialise la variable privée '_normalize_weights' de l'instance
#         courante.
#
#         Si le node courant n'existe pas, la variable privée _normalize_weights
#         est initialisée à False.
#         Sinon, la variable privée _normalize_weights est initialisée à la
#         valeur de l'attribut 'normalizeWeights' du node courant.
#
#         Returns:
#             None
#         """
#         if self.exists:
#             norm_weights = self.plugs.get_plug("normalizeWeights").asBool()
#
#         elif (hasattr(self, "_normalize_weights") and
#               self._normalize_weights is not None):
#             norm_weights = self._normalize_weights
#         else:
#             norm_weights = False
#
#         return norm_weights
#
#     def _init_weight_distribution(
#         self
#     ) -> int:
#
#         """
#         Initialise la variable privée '_weight_distribution' de l'instance
#         courante.
#
#         Si le node courant n'existe pas, la variable privée
#         _weight_distribution est initialisée à 0.
#         Sinon, la variable privée _weight_distribution est initialisée à la
#         valeur de l'attribut 'weightDistribution' du node courant.
#
#         Returns:
#             None
#         """
#
#         return (
#             self.get_int_attr("weightDistribution")
#             if self.exists
#             else (
#                 (
#                         self._weight_distribution
#                         if self._weight_distribution is not None
#                         else 0
#                 )
#                 if hasattr(self, "_weight_distribution")
#                 else 0
#             )
#         )
#
#     def _default_weights(
#         self
#     ) -> om.MDoubleArray:
#
#         """
#         Renvoie la liste des weights par défaut du node courant.
#
#         Returns:
#             om.MDoubleArray
#                 La liste des weights par défaut du node courant.
#         """
#
#         return om.MDoubleArray(
#             [
#                 (
#                     1.0
#                     if i < self.output_components_count
#                     else 0.0
#                 )
#                 for i in range(
#                     self.influences_len*self.output_components_count
#                 )
#             ]
#         ) if self.has_output_geometries and self.influences_len > 0 else (
#             om.MDoubleArray()
#         )
#
# # - SkinCluster Fn ------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def _init_skincluster_fn(
#         self
#     ) -> None:
#
#         """
#         Initialise l'objet MFnSkinCluster de l'instance courante.
#
#         Returns:
#             None
#         """
#
#         self._skincluster_fn = (
#             oma.MFnSkinCluster(self.maya_object)
#             if self.exists
#             else None
#         )
#
# # - Influence Objects ---------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def _init_influence_objects(
#         self,
#         influence_objects: Optional[Union[
#             om.MDagPathArray,
#             List[om.MDagPath],
#             List[Type[dagLib.DAGNode]],
#             List[str],
#             om.MDagPath,
#             Type[dagLib.DAGNode],
#             str
#         ]] = None
#     ) -> None:
#
#         """
#         Initialise la liste des influence objects de l'instance courante.
#
#         Args:
#             influence_objects (Optional[Union[
#                 om.MDagPathArray,
#                 List[om.MDagPath],
#                 List[lib_nde.Node],
#                 List[str],
#                 om.MDagPath,
#                 lib_nde.Node,
#                 str
#             ]], optional):
#                 Les influence objects à initialiser.
#
#         Returns:
#             None
#         """
#
#         if not self.exists and influence_objects is None:
#             self._influence_objects = influence_objects
#             return
#
#         self._influence_objects = (
#             self.skincluster_fn.influenceObjects()
#             if self.exists
#             and self.plugs.get_plug('matrix').numElements() > 0
#             else om.MDagPathArray()
#         )
#
#     def _disconnect_influence_objects(
#         self
#     ) -> None:
#
#         """
#         Déconnecte les influence objects de l'instance courante.
#
#         Returns:
#             None
#         """
#
#         attrs = [
#             "influenceColor",
#             "lockWeights",
#             "matrix"
#         ]
#
#         for attr in attrs:
#             plug = self.plugs.get_plug(attr)
#             num = plug.numElements()
#             for i in range(num):
#                 sub_plug = plug.elementByPhysicalIndex(0)
#                 if plug.isConnected:
#                     self.disconnect_attr(sub_plug.source(), sub_plug)
#
#     def _disconnect_influence_object(
#         self,
#         influence_object: Optional[om.MDagPath] = None,
#         index: Optional[int] = None
#     ) -> None:
#
#         """
#         Déconnecte l'influence object spécifié de l'instance courante.
#
#         Args:
#             influence_object (Optional[om.MDagPath], optional):
#                 L'influence object à déconnecter.
#
#             index (Optional[int], optional):
#                 L'index de l'influence object à déconnecter.
#
#         Returns:
#             None
#         """
#
#         if influence_object is None or index is None:
#             return
#
#         influence_object = influence_object.partialPathName()
#
#         attrs = [
#             "influenceColor",
#             "lockWeights",
#             "matrix"
#         ]
#
#         for attr in attrs:
#             plug = self.plugs.get_plug(attr).elementByPhysicalIndex(index)
#
#             if plug.isConnected:
#                 self.disconnect_attr(plug.source(), plug)
#
#     def _connect_influence_objects(
#         self,
#         influence_objects: om.MDagPathArray
#     ) -> None:
#
#         """
#         Connecte les influence objects de l'instance courante.
#
#         Returns:
#             None
#         """
#
#         for i in range(len(influence_objects)):
#
#             self._connect_influence_object(
#                 influence_objects[i],
#                 i
#             )
#
#     def _connect_influence_object(
#         self,
#         influence_object: om.MDagPath,
#         index: int
#     ) -> None:
#
#         """
#         Connecte l'influence object spécifié à l'instance courante.
#
#         Args:
#             influence_object (om.MDagPath):
#                 L'influence object à connecter.
#
#             index (int):
#                 L'index de l'influence object à connecter.
#
#         Returns:
#             None
#         """
#
#         index = str(index)
#         influence_object = influence_object.partialPathName()
#
#         self.connect_attr(
#             f"{influence_object}.objectColorRGB",
#             f"{self.name}.influenceColor[{index}]"
#         )
#
#         self.connect_attr(
#             f"{influence_object}.worldMatrix[0]",
#             f"{self.name}.matrix[{index}]"
#         )
#
#         self._check_influence_lock_attr(
#             influence_object
#         )
#
#         self.connect_attr(
#             f"{influence_object}.lockInfluenceWeights",
#             f"{self.name}.lockWeights[{index}]"
#         )
#
#     @staticmethod
#     def _check_influence_lock_attr(
#         influence_object: str
#     ) -> None:
#
#         """
#         Vérifie si l'attribut 'lockInfluenceWeights' de l'objet influence
#         spécifié existe et le crée si nécessaire.
#
#         Args:
#             influence_object (str):
#                 L'objet influence à vérifier.
#
#         Returns:
#             None
#         """
#
#         influence_object = dagLib.DAGNode(influence_object)
#
#         if "lockInfluenceWeights" not in (
#             influence_object.plugs.attribute_names
#         ):
#
#             influence_object.plugs.add_bool_plug(
#                 "lockInfluenceWeights",
#                 "lockInfluenceWeights",
#                 False
#             )
#
# # - Skinning Method -----------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def _init_skinning_method(
#         self
#     ) -> None:
#
#         """
#         Initialise la variable privée '_skinning_method' de l'instance
#         courante.
#
#         Si le node courant n'existe pas, la variable privée '_skinning_method'
#         est initialisée à 0. Sinon, la variable privée '_skinning_method' est
#         initialisée à la valeur de l'attribut 'skinningMethod' du node courant.
#
#         Returns:
#             None
#         """
#
#         return (
#             self.plugs.get_plug("skinningMethod").asShort()
#             if self.exists
#             else (
#                 self._skinning_method
#                 if hasattr(self, "_skinning_method")
#                 else 0
#             )
#         )
#
#     def _check_skinning_method(
#         self,
#         skinning_method: Union[int, str]
#     ) -> int:
#
#         """
#         Vérifie si la méthode de skinning spécifiée est valide.
#
#         Args:
#             skinning_method (int):
#                 La méthode de skinning à vérifier.
#
#         Raises:
#             ValueError:
#                 Si la méthode de skinning spécifiée est invalide.
#
#         Returns:
#             int
#                 La méthode de skinning.
#         """
#
#         if isinstance(skinning_method, str):
#             skinning_method = self._convert_skinning_method_str_to_int(
#                 skinning_method
#             )
#
#         if skinning_method not in [0, 1, 2]:
#
#             raise ValueError(
#                 "Error while setting skinning_method:"
#                 f"\n - Invalid skinning method: {skinning_method}"
#                 "\n - Valid skinning methods (int): "
#                 "\n - (0: linear),"
#                 "\n - (1: dual quaternion),"
#                 "\n - (2: blended)"
#             )
#
#         return skinning_method
#
# # - Components ----------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def _init_use_components(
#         self
#     ) -> None:
#
#         """
#         Initialise la variable privée '_use_components' de l'instance courante.
#
#         Si le node courant n'existe pas, la variable privée '_use_components'
#         est initialisée à False. Sinon, la variable privée '_use_components'
#         est initialisée à la valeur de l'attribut 'useComponents' du node
#         courant.
#
#         Returns:
#             None
#         """
#
#         return (
#             self.plugs.get_plug("useComponents").asBool()
#             if self.exists
#             else (
#                 self._use_components
#                 if hasattr(self, "_use_components")
#                 else False
#             )
#         )
#
# # - DQS -----------------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def _init_dqs_support_nonRigid(
#         self
#     ) -> None:
#
#         """
#         Initialise la variable privée '_dqs_support_nonRigid' de l'instance
#         courante.
#
#         Si le node courant n'existe pas, la variable privée
#         '_dqs_support_nonRigid' est initialisée à False.
#         Sinon, la variable privée '_dqs_support_nonRigid' est
#         initialisée à la valeur de l'attribut 'dqsSupportNonRigid'
#         du node courant.
#
#         Returns:
#             None
#         """
#
#         return (
#             self.plugs.get_plug("dqsSupportNonRigid").asBool()
#             if self.exists
#             else (
#                 self._dqs_support_nonRigid
#                 if hasattr(self, "_dqs_support_nonRigid")
#                 else False
#             )
#         )
#
#     def _get_dqs_scale_value(
#         self,
#         attr_name: str
#     ) -> float:
#
#         """
#         Renvoie la valeur de l'attribut spécifié.
#
#         Args:
#             attr_name (str):
#                 Le nom de l'attribut à renvoyer.
#
#         Returns:
#             float
#         """
#
#         return (
#             self.plugs.get_plug(attr_name).asFloat()
#             if self.exists
#             else (
#                 getattr(self, f"_dqs_scale{attr_name[-1]}")
#                 if hasattr(self, f"_dqs_scale{attr_name[-1]}")
#                 else 1.0
#             )
#         )
#
# # - Max Influences ------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def _init_max_influences(
#         self
#     ) -> None:
#
#         """
#         Initialise la variable privée '_max_influences' de l'instance courante.
#
#         Si le node courant n'existe pas, la variable privée '_max_influences'
#         est initialisée à False. Sinon, la variable privée '_max_influences'
#         est initialisée à la valeur de l'attribut 'maxInfluences' du node
#         courant.
#
#         Returns:
#             None
#         """
#
#         return (
#             self.plugs.get_plug("maxInfluences").asInt()
#             if self.exists
#             else (
#                 self._max_influences
#                 if hasattr(self, "_max_influences")
#                 else 5
#             )
#         )
#
#     def _init_maintain_max_influences(
#         self
#     ) -> None:
#
#         """
#         Initialise la variable privée '_maintain_max_influences' de l'instance
#         courante.
#
#         Si le node courant n'existe pas, la variable privée
#         '_maintain_max_influences' est initialisée à False. Sinon, la variable
#         privée '_maintain_max_influences' est initialisée à la valeur de
#         l'attribut 'maintainMaxInfluences' du node courant.
#
#         Returns:
#             None
#         """
#
#         return (
#             self.plugs.get_plug("maintainMaxInfluences").asBool()
#             if self.exists
#             else (
#                 self._maintain_max_influences
#                 if hasattr(self, "_maintain_max_influences")
#                 else False
#             )
#         )
#
# # - Attributes ----------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def _init_deform_user_normals(
#         self
#     ) -> None:
#
#         """
#         Initialise la variable privée '_deform_user_normals' de l'instance
#         courante.
#
#         Si le node courant n'existe pas, la variable privée
#         '_deform_user_normals' est initialisée à False. Sinon, la variable
#         privée '_deform_user_normals' est initialisée à la valeur de l'attribut
#         'deformUserNormals' du node courant.
#
#         Returns:
#             None
#         """
#
#         return (
#             self.plugs.get_plug("deformUserNormals").asBool()
#             if self.exists
#             else (
#                 self._deform_user_normals
#                 if hasattr(self, "_deform_user_normals")
#                 else False
#             )
#         )
#
#     def _check_normalize_weights(
#         self,
#         normalize_weights: Union[int, str]
#     ) -> int:
#
#         """
#         Vérifie si la valeur de l'attribut 'normalizeWeights' spécifiée est
#         valide.
#
#         Args:
#             normalize_weights (Union[int, str]):
#                 La valeur de l'attribut 'normalizeWeights' à vérifier.
#
#         Raises:
#             ValueError:
#                 Si la valeur de l'attribut 'normalizeWeights' spécifiée est
#                 invalide.
#
#         Returns:
#             int
#                 La valeur de l'attribut 'normalizeWeights'.
#         """
#
#         if isinstance(normalize_weights, str):
#             self._convert_normalize_weights_str_to_int(
#                 normalize_weights
#             )
#
#         if normalize_weights not in [0, 1, 2]:
#
#             raise ValueError(
#                 "Error while setting normalize_weights:"
#                 f"\n - Invalid normalize_weights: {normalize_weights}"
#                 "\n - Valid normalize_weights (int): "
#                 "\n - (0: none),"
#                 "\n - (1: interactive),"
#                 "\n - (2: post)"
#             )
#
#         return normalize_weights
#
#     def _check_weight_distribution(
#         self,
#         weight_distribution: Union[int, str]
#     ) -> int:
#
#         """
#         Vérifie si la méthode de distribution des weights spécifiée est valide.
#
#         Args:
#             weight_distribution (Union[int, str]):
#                 La méthode de distribution des weights à vérifier.
#
#         Raises:
#             ValueError:
#                 Si la méthode de distribution des weights spécifiée est
#                 invalide.
#
#         Returns:
#             int
#                 La méthode de distribution des weights.
#         """
#
#         if isinstance(weight_distribution, str):
#             weight_distribution = self._convert_weight_distribution_str_to_int(
#                 weight_distribution
#             )
#
#         if weight_distribution not in [0, 1]:
#
#             raise ValueError(
#                 "Error while setting weight_distribution:"
#                 f"\n - Invalid weight_distribution: {weight_distribution}"
#                 "\n - Valid weight_distribution (int): "
#                 "\n - (0: Distance),"
#                 "\n - (1: Neighbors)"
#             )
#
#         return weight_distribution
#
# # - Validation ----------------------------------------------------------------
# # -----------------------------------------------------------------------------
#
#     @staticmethod
#     def _convert_skinning_method_str_to_int(
#         skinning_method: str
#     ) -> int:
#
#         """
#         Convertit la méthode de skinning spécifiée en int.
#
#         Args:
#             skinning_method (str):
#                 La méthode de skinning à convertir.
#
#         Returns:
#             int
#         """
#
#         if (
#             "linear" in skinning_method.lower()
#             or "classic" in skinning_method.lower()
#         ):
#
#             return 0
#
#         elif (
#             "dual" in skinning_method.lower()
#             or "quat" in skinning_method.lower()
#         ):
#
#             return 1
#
#         elif (
#             "blend" in skinning_method.lower()
#             or "weight" in skinning_method.lower()
#         ):
#
#             return 2
#
#         else:
#
#             return skinning_method
#
#     @staticmethod
#     def _convert_normalize_weights_str_to_int(
#         normalize_weights: str
#     ) -> int:
#
#         """
#         Convertit la valeur de l'attribut 'normalizeWeights' spécifiée en int.
#
#         Args:
#             normalize_weights (str):
#                 La valeur de l'attribut 'normalizeWeights' à convertir.
#
#         Returns:
#             int
#                 La valeur de l'attribut 'normalizeWeights'.
#         """
#
#         if "no" in normalize_weights.lower():
#
#             return 0
#
#         elif (
#             "inter" in normalize_weights.lower()
#             or "active" in normalize_weights.lower()
#         ):
#
#             return 1
#
#         elif "post" in normalize_weights.lower():
#
#             return 2
#
#         else:
#             return normalize_weights
#
#     @staticmethod
#     def _convert_weight_distribution_str_to_int(
#         weight_distribution: str
#     ) -> int:
#
#         """
#         Convertit la méthode de distribution des weights spécifiée en int.
#
#         Args:
#             weight_distribution (str):
#                 La méthode de distribution des weights à convertir.
#
#         Returns:
#             int
#                 La méthode de distribution des weights.
#         """
#
#         if "dist" in weight_distribution.lower():
#
#             return 0
#
#         elif "neigh" in weight_distribution.lower():
#
#             return 1
#
#         else:
#
#             return weight_distribution
#
#     @staticmethod
#     def _get_component_type_str(
#         component_type: int
#     ) -> str:
#
#         """
#         Renvoie le nom du type de composant spécifié.
#
#         Args:
#             component_type (int):
#                 Le type de composant à renvoyer.
#
#         Returns:
#             str
#         """
#
#         if component_type == om.MFn.kMesh:
#             return "vtx"
#
#         elif component_type in [om.MFn.kNurbsSurface, om.MFn.kNurbsCurve]:
#
#             return "cv"
#
#         elif component_type == om.MFn.kLattice:
#
#             return "pt"
#
#         else:
#
#             raise ValueError(
#                 "Error while getting component type str:"
#                 f"\n - Invalid component type: {component_type}"
#             )


NodeRegistry()[SkinCluster.nodeType()] = SkinCluster
