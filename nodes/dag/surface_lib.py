from typing import List, Union, Sequence, Optional, Callable, Tuple

from maya import cmds as mc
from maya.api import OpenMaya as om

from ...core import convert
from ...core.abstract import dag_lib
from ...core.node_registry import NodeRegistry


class Surface(dag_lib.DAGNode):

    _NODE_TYPE = "nurbsSurface"
    _API_TYPE = om.MFn.kNurbsSurface

    def __init__(self, name: str = None) -> None:

        """
        Initialize an instance of Surface

        Args:
            name: Optional[str], the name of the node
        """

        self._is_shape = True

        super().__init__(name=name)

        self._init_surface_properties()

    @property
    def mfnNurbsSurface(self) -> om.MFnNurbsSurface:

        """
        Récupère l'API MFnNurbsSurface du node.

        Returns
            om.MFnNurbsSurface
                API MFnNurbsSurface du node.
        """

        return om.MFnNurbsSurface(self)

#     @property
#     def area(self) -> float:
#
#         """
#         Get the surface arra
#
#         Returns:
#             float: the areo of the surface
#         """
#
#         return self.mfnNurbsSurface.area()
#
#     @property
#     def numPatches(self) -> int:
#
#         """
#         Get the number of patches of the surface
#
#         Returns:
#             int: the number of surface patches
#         """
#
#         return self.mfnNurbsSurface.numPatches
#
#     @property
#     def numPatchesInU(self) -> int:
#
#         """
#         Get the number of surface patches in U direction
#
#         Returns:
#             int: the number of surface patches in U direction
#         """
#
#         return self.mfnNurbsSurface.numPatchesInU
#
#     @property
#     def numPatchesInV(self) -> int:
#
#         """
#         Get the number of surface patches in V direction
#
#         Returns:
#             int: the number of surface patches in V direction
#         """
#
#         return self.mfnNurbsSurface.numPatchesInV
#
#     @property
#     def numSpansInU(self) -> int:
#
#         """
#         Get the number of spans in U direction
#
#         Returns:
#             int: the number of spans in U direction
#         """
#
#         return self.mfnNurbsSurface.numSpansInU
#
#     @property
#     def numSpansInV(self) -> int:
#
#         """
#         Get the number of spans in V direction
#
#         Returns:
#             int: the number of spans in V direction
#         """
#
#         return self.mfnNurbsSurface.numSpansInV
#
#     @property
#     def spanIndicesInU(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
#
#         """
#         Get the span indices in U direction
#
#         Returns
#             List[Tuple[Tuple[int, int]]]: a list of tuples describing U spans
#                 in the form of tuples of indices
#         """
#
#         spanIndices = []
#
#         for vIndex in range(self.numSpansInV + 1):
#             for uIndex in range(self.numSpansInU):
#                 spanIndices.append(((uIndex, vIndex), (uIndex + 1, vIndex)))
#
#         return spanIndices
#
#     @property
#     def spanIndicesInV(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
#
#         """
#         Get the span indices in V direction
#
#         Returns
#             List[Tuple[Tuple[int, int]]]: a list of tuples describing V spans
#                 in the form of tuples of indices
#         """
#
#         spanIndices = []
#
#         for uIndex in range(self.numSpansInU + 1):
#             for vIndex in range(self.numSpansInV):
#                 spanIndices.append(((uIndex, vIndex), (uIndex, vIndex + 1)))
#
#         return spanIndices
#
#     @property
#     def spanPointsInU(self) -> List[Tuple[Tuple[om.MPoint, om.MPoint]]]:
#
#         """
#         Get span points positions in U direction
#
#         Returns
#             List[Tuple[Tuple[int, int]]]: a list of tuples describing U spans
#                 in the form of tuples of points
#         """
#
#         spanPoints = []
#
#         for edge in self.spanIndicesInU:
#             spanPoints.append(
#                 (
#                     self.get_cv_position(edge[0][0], edge[0][1]),
#                     self.get_cv_position(edge[1][0], edge[1][1])
#                 )
#             )
#
#         return spanPoints
#
#     @property
#     def spanPointsInV(self) -> List[Tuple[Tuple[om.MPoint, om.MPoint]]]:
#
#         """
#         Get span points positions in V direction
#
#         Returns
#             List[Tuple[Tuple[int, int]]]: a list of tuples describing V spans
#                 in the form of tuples of points
#         """
#
#         spanPoints = []
#
#         for edge in self.spanIndicesInV:
#             spanPoints.append(
#                 (
#                     self.get_cv_position(edge[0][0], edge[0][1]),
#                     self.get_cv_position(edge[1][0], edge[1][1])
#                 )
#             )
#
#         return spanPoints
#
#     @property
#     def cvsList(self) -> List[Tuple[Tuple[int, int], om.MObject]]:
#
#         """
#         Get surfaces cvs in a formatted structure
#
#         Returns
#             List[Tuple[Tuple[int, int], om.MObject]]: A list of typle containing
#                 a tuple of indices and the cv om.MObject
#         """
#
#         return [
#             ((uIndex, vIndex), self.cv(uIndex, vIndex))
#             for uIndex in range(self.u_spans + self.u_degree)
#             for vIndex in range(self.v_spans + self.v_degree)
#         ]
#
#     @property
#     def numCVsInU(self) -> int:
#
#         """
#         Get the number of CVs in U direction
#
#         Returns:
#             int: the number of CVs in U direction
#         """
#
#         return self.mfnNurbsSurface.numCVsInU
#
#     @property
#     def numCVsInV(self) -> int:
#
#         """
#         Get the number of CVs in V direction
#
#         Returns:
#             int: the number of CVs in V direction
#         """
#
#         return self.mfnNurbsSurface.numCVsInV
#
#     @property
#     def cvs(self) -> om.MPointArray:
#
#         """
#         Récupère les points de la surface.
#         Si le node n'existe pas, retourne une liste vide.
#         Si le node existe mais qu'il n'a pas de points,
#         retourne une liste vide.
#
#         Returns
#         -------
#         om.MPointArray
#             Points de la surface.
#         """
#
#         return (
#             self.get_cvs()
#             if self.exists
#             else self._cvs
#         )
#
#     @cvs.setter
#     def cvs(
#         self,
#         points: Optional[Union[
#             om.MPointArray,
#             List[om.MPoint],
#             List[List[float]]
#         ]] = None
#     ) -> None:
#
#         """
#         Définit les points de la surface.
#
#         Parameters
#         ----------
#         points : Union[om.MPointArray, List[om.MPoint], List[List[float]]]
#             Points de la surface.
#             Peut être une liste de MPoint, une liste de listes de float,
#             ou une MPointArray.
#
#         Returns
#         -------
#         None
#         """
#
#         if points is None:
#             self._cvs = om.MPointArray()
#             self.shape_orig._cvs = om.MPointArray()
#             return
#
#         points = convert.to_mpointarray(points)
#
#         self._cvs = points
#         self.shape_orig._cvs = points
#
#     @property
#     def len_cvs(
#         self
#     ) -> int:
#
#         """
#         Récupère le nombre de points de la surface.
#
#         Returns
#         -------
#         int
#             Nombre de points de la surface.
#         """
#
#         return len(self.cvs) or 0
#
# # - Degree --------------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     @property
#     def u_degree(
#         self
#     ) -> int:
#
#         """
#         Récupère le degré en U de la surface.
#
#         Returns
#         -------
#         int
#             Degré en U de la surface.
#         """
#
#         return (
#             self.get_u_degree()
#             if self.exists
#             else self._u_degree
#         )
#
#     @u_degree.setter
#     def u_degree(
#         self,
#         degree: int
#     ) -> None:
#
#         """
#         Définit le degré en U de la surface.
#
#         Parameters
#         ----------
#         degree : int
#             Degré en U de la surface.
#
#         Returns
#         -------
#         None
#         """
#
#         if degree == self.u_degree:
#             return
#
#         self._set_surface_attribute(
#             "u",
#             "degree",
#             degree,
#             self.set_u_degree
#         )
#
#     @property
#     def v_degree(
#         self
#     ) -> int:
#
#         """
#         Récupère le degré en V de la surface.
#
#         Returns
#         -------
#         int
#             Degré en V de la surface.
#         """
#
#         return (
#             self.get_v_degree()
#             if self.exists
#             else self._v_degree
#         )
#
#     @v_degree.setter
#     def v_degree(
#         self,
#         degree: int
#     ) -> None:
#
#         """
#         Définit le degré en V de la surface.
#
#         Parameters
#         ----------
#         degree : int
#             Degré en V de la surface.
#
#         Returns
#         -------
#         None
#         """
#
#         if degree == self.v_degree:
#             return
#
#         self._set_surface_attribute(
#             "v",
#             "degree",
#             degree,
#             self.set_v_degree
#         )
#
# # - Spans ---------------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     @property
#     def u_spans(
#         self
#     ) -> int:
#
#         """
#         Récupère le nombre de spans en U de la surface.
#
#         Returns
#         -------
#         int
#             Nombre de spans en U de la surface.
#         """
#
#         return (
#             self.get_u_spans()
#             if self.exists
#             else self._u_spans
#         )
#
#     @u_spans.setter
#     def u_spans(
#         self,
#         spans: int
#     ) -> None:
#
#         """
#         Définit le nombre de spans en U de la surface.
#
#         Parameters
#         ----------
#         spans : int
#             Nombre de spans en U de la surface.
#
#         Returns
#         -------
#         None
#         """
#
#         if spans == self.u_spans:
#             return
#
#         self._set_surface_attribute(
#             "u",
#             "spans",
#             spans,
#             self.set_u_spans
#         )
#
#     @property
#     def v_spans(
#         self
#     ) -> int:
#
#         """
#         Récupère le nombre de spans en V de la surface.
#
#         Returns
#         -------
#         int
#             Nombre de spans en V de la surface.
#         """
#
#         return (
#             self.get_v_spans()
#             if self.exists
#             else self._v_spans
#         )
#
#     @v_spans.setter
#     def v_spans(
#         self,
#         spans: int
#     ) -> None:
#
#         """
#         Définit le nombre de spans en V de la surface.
#
#         Parameters
#         ----------
#         spans : int
#             Nombre de spans en V de la surface.
#
#         Returns
#         -------
#         None
#         """
#
#         if spans == self.v_spans:
#             return
#
#         self._set_surface_attribute(
#             "v",
#             "spans",
#             spans,
#             self.set_v_spans
#         )
#
# # - Knots ---------------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     @property
#     def u_knots(
#         self
#     ) -> om.MDoubleArray:
#
#         """
#         Récupère les knots en U de la surface.
#
#         Returns
#         -------
#         om.MDoubleArray
#             Knots en U de la surface.
#         """
#
#         return (
#             self.get_u_knots()
#             if self.exists
#             else self._u_knots
#         )
#
#     @u_knots.setter
#     def u_knots(
#         self,
#         knots: Union[om.MDoubleArray, Sequence[float]]
#     ) -> None:
#
#         """
#         Définit les knots en U de la surface.
#
#         Parameters
#         ----------
#         knots : Union[om.MDoubleArray, Sequence[float]]
#             Knots en U de la surface.
#             Peut être une om.MDoubleArray ou une liste de float.
#
#         Returns
#         -------
#         None
#         """
#
#         knots = convert.to_MDoubleArray(knots)
#         self._u_knots = knots
#         self.shape_orig._u_knots = knots
#
#     @property
#     def v_knots(
#         self
#     ) -> om.MDoubleArray:
#
#         """
#         Récupère les knots en V de la surface.
#
#         Returns
#         -------
#         om.MDoubleArray
#             Knots en V de la surface.
#         """
#
#         return (
#             self.get_v_knots()
#             if self.exists
#             else self._v_knots
#         )
#
#     @v_knots.setter
#     def v_knots(
#         self,
#         knots: Union[om.MDoubleArray, Sequence[float]]
#     ) -> None:
#
#         """
#         Définit les knots en V de la surface.
#
#         Parameters
#         ----------
#         knots : Union[om.MDoubleArray, Sequence[float]]
#             Knots en V de la surface.
#             Peut être une om.MDoubleArray ou une liste de float.
#
#         Returns
#         -------
#         None
#         """
#
#         knots = convert.to_MDoubleArray(knots)
#         self._v_knots = knots
#         self.shape_orig._v_knots = knots
#
# # - Form ----------------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     @property
#     def u_form(
#         self
#     ) -> int:
#
#         """
#         Récupère la forme en U de la surface.
#         0 = Invalide, 1 = Open, 2 = Close, 3 = Periodic.
#
#         Returns
#         -------
#         int
#             Forme en U de la surface.
#         """
#
#         return (
#             self.get_u_form()
#             if self.exists
#             else self._u_form
#         )
#
#     @u_form.setter
#     def u_form(
#         self,
#         form: int
#     ) -> None:
#
#         """
#         Définit la forme en U de la surface.
#
#         Parameters
#         ----------
#         form : int
#             Forme en U de la surface.
#             0 = Invalid
#             1 = Open
#             2 = Closed
#             3 = Periodic
#
#         Returns
#         -------
#         None
#         """
#
#         self._u_form = form
#         self.shape_orig._u_form = form
#
#     @property
#     def v_form(
#         self
#     ) -> int:
#
#         """
#         Récupère la forme en V de la surface.
#         0 = Invalide, 1 = Open, 2 = Close, 3 = Periodic.
#
#         Returns
#         -------
#         int
#             Forme en V de la surface.
#         """
#
#         return (
#             self.get_v_form()
#             if self.exists
#             else self._v_form
#         )
#
#     @v_form.setter
#     def v_form(
#         self,
#         form: int
#     ) -> None:
#
#         """
#         Définit la forme en V de la surface.
#
#         Parameters
#         ----------
#         form : int
#             Forme en V de la surface.
#             0 = Invalid
#             1 = Open
#             2 = Closed
#             3 = Periodic
#
#         Returns
#         -------
#         None
#         """
#
#         self._v_form = form
#         self.shape_orig._v_form = form
#
# # - Spans ---------------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     @property
#     def is_uniform(
#         self
#     ) -> bool:
#
#         """
#         Retourne True si la surface est uniforme,
#         False si elle est non uniforme, c'est à dire
#         si elle a des spans de tailles différentes.
#
#         Returns
#         -------
#         bool
#             Si la surface est uniforme.
#         """
#
#         return (
#             self._get_is_uniform()
#             if self.exists
#             else self._is_uniform
#         )
#
#     @is_uniform.setter
#     def is_uniform(
#         self,
#         value: bool
#     ) -> None:
#
#         """
#         Définit si la surface est uniforme.
#
#         Parameters
#         ----------
#         value : bool
#             Si la surface est uniforme.
#
#         Returns
#         -------
#         None
#         """
#
#         self._is_uniform = value
#         self.shape_orig._is_uniform = value
#
#     @property
#     def is_rational(
#         self
#     ) -> bool:
#
#         """
#         Retourne True si la surface est rationnelle,
#         False si elle est non rationnelle, c'est à dire
#         si elle a des poids différents.
#
#         Returns
#         -------
#         bool
#             Si la surface est rationnelle.
#         """
#
#         return self._is_rational
#
#     @is_rational.setter
#     def is_rational(
#         self,
#         value: bool
#     ) -> None:
#
#         """
#         Définit si la surface est rationnelle.
#
#         Parameters
#         ----------
#         value : bool
#             Si la surface est rationnelle.
#
#         Returns
#         -------
#         None
#         """
#
#         self._is_rational = value
#         self.shape_orig._is_rational = value
#
# # - Boundaries & Regions ------------------------------------------------------
# # -----------------------------------------------------------------------------
#     @property
#     def is_trimmed(
#         self
#     ) -> bool:
#
#         """
#         Retourne True si la surface est trimmée,
#         False si elle ne l'est pas.
#
#         Returns
#             bool
#                 Si la surface est trimmée.
#         """
#
#         return self.mfnNurbsSurface.isTrimmedSurface if self.exists else False
#
#     @property
#     def len_regions(
#         self
#     ) -> int:
#
#         """
#         Récupère le nombre de régions de la surface.
#
#         Returns
#         -------
#         int
#             Nombre de régions de la surface.
#         """
#
#         return self.mfnNurbsSurface.numRegions if self.exists else 0
#
#     @property
#     def boundary_per_region(
#         self
#     ) -> List[int]:
#
#         """
#         Récupère les bords par région de la surface.
#
#         Returns
#         -------
#         List[int]
#             Bords par région de la surface.
#         """
#
#         return (
#             [
#                 self.mfnNurbsSurface.numBoundaries(i)
#                 for i in range(self.len_regions)
#             ]
#             if self.exists
#             else []
#         )
#
# #     def create(
# #         self
# #     ) -> om.MObject:
# #
# #         """
# #         Crée une surface.
# #         Les points de la surface doivent être définis avant.
# #         Les knots de la surface doivent être définis avant.
# #         Le degré de la surface doit être défini avant.
# #         La forme de la surface doit être définie avant.
# #         Aussi, la surface ne doit pas déjà exister.
# #
# #         Returns
# #         -------
# #         om.MObject
# #             Nouvelle surface créée.
# #         """
# #
# #         if self.exists:
# #             return
# #
# #         u_form = convert.int_to_form(self.u_form)
# #         v_form = convert.int_to_form(self.v_form)
# #
# #         surface_fn = om.MFnNurbsSurface()
# #         surface_fn.create(
# #             self.cvs,
# #             self.u_knots,
# #             self.v_knots,
# #             self._u_degree,
# #             self._v_degree,
# #             u_form,
# #             v_form,
# #             self.is_rational
# #         )
# #
# #         surface_fn.setName(self.name)
# #
# #         if (
# #             self.is_orig
# #             or (
# #                 self.parent is not None
# #                 and self.parent.exists
# #             )
# #         ):
# #             old_parent = self.maya_dagNode.parent(0)
# #             om.MDagModifier().reparentNode(
# #                 self.maya_object,
# #                 self.parent.maya_object
# #             ).doIt()
# #             om.MGlobal.deleteNode(old_parent)
# #
# #         else:
# #             parent = dag_lib.DAGNode(
# #                 self.name.replace(
# #                     "_nrbSrf",
# #                     "_srf"
# #                 ) if "_nrbSrf" in self.name else (
# #                     self.name + "_srf"
# #                 )
# #             )
# #             mc.rename(
# #                 om.MFnDagNode(
# #                     self.maya_dagNode.parent(0)
# #                 ).partialPathName(),
# #                 parent.name
# #             )
# #             self._init_parent()
# #             self.shape_orig.parent = parent
# #
# #         self.plugs.refresh()
# #
# #         if self.is_orig:
# #             self.plugs.set_bool("intermediateObject", True)
# #
# #         self._surface_fn = om.MFnNurbsSurface(self.maya_object)
#
#     def copy(
#         self
#     ) -> om.MObject:
#
#         """
#         Copie la surface.
#
#         Returns
#         -------
#         om.MObject
#             Nouvelle surface copiée.
#         """
#
#         return self.mfnNurbsSurface.copy(self.maya_object)
#
# # - Closest -------------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def closest_point(
#         self,
#         point: om.MPoint,
#         space: om.MSpace = None
#     ) -> om.MPoint:
#
#         """
#         Récupère le point de la surface le plus proche du point donné.
#
#         Args:
#             point (om.MPoint):
#                 Point à cibler.
#
#             space (om.MSpace, optional):
#                 Espace dans lequel récupérer le point le plus proche.
#
#         Returns
#             om.MPoint:
#                 Point de la surface le plus proche du point donné.
#         """
#
#         if space is None:
#             space = om.MSpace.kWorld
#
#         return self.mfnNurbsSurface.closestPoint(
#             point,
#             uStart=None,
#             vStart=None,
#             ignoreTrimBoundaries=False,
#             tolerance=0
#         )[0]
#
#     def closest_param(
#         self,
#         point: om.MPoint,
#         space: om.MSpace = None
#     ) -> Tuple[float, float]:
#
#         """
#         Récupère les paramètres U et V de la surface donnant
#         le point le plus proche du point donné.
#
#         Args:
#             point (om.MPoint):
#                 Point à partir duquel récupérer les paramètres U et V.
#
#             space (om.MSpace, optional):
#                 Espace dans lequel récupérer les paramètres U et V.
#
#         Returns
#             Tuple[float, float]:
#                 Paramètres U et V de la surface donnant le point le plus proche
#                 du point donné.
#         """
#
#         if space is None:
#             space = om.MSpace.kWorld
#
#         return self.mfnNurbsSurface.closestPoint(
#             point,
#             uStart=None,
#             vStart=None,
#             ignoreTrimBoundaries=False,
#             tolerance=0
#         )[1:3]
#
# # - Parameters ----------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def get_param_at_point(
#         self,
#         point: om.MPoint,
#         ignore_trim: bool = False,
#         tolerance: float = None,
#         space: om.MSpace = None
#     ) -> Tuple[float, float]:
#
#         """
#         Récupère les paramètres U et V de la surface à partir d'un point.
#
#         Args:
#             point (om.MPoint):
#                 Point à partir duquel récupérer les paramètres U et V.
#
#             space (om.MSpace, optional):
#                 Espace dans lequel récupérer les paramètres U et V.
#
#         Returns
#             Tuple[float, float]:
#                 Paramètres U et V de la surface.
#         """
#
#         if space is None:
#             space = om.MSpace.kWorld
#
#         if tolerance is None:
#             tolerance = 1e-3
#
#         return self.mfnNurbsSurface.getParamAtPoint(
#             point,
#             ignore_trim,
#             tolerance,
#             space
#         )
#
#     def get_point_at_param(
#         self,
#         u: float,
#         v: float
#     ) -> om.MPoint:
#
#         """
#         Récupère un point de la surface à partir de paramètres U et V.
#
#         Args:
#             u (float):
#                 Paramètre U du point à récupérer.
#
#             v (float):
#                 Paramètre V du point à récupérer.
#
#         Returns
#             om.MPoint:
#                 Point de la surface.
#         """
#
#         return self.mfnNurbsSurface.getPointAtParam(u, v)
#
#     def intersect(
#         self,
#         ray_start: om.MPoint,
#         ray_dir: om.MVector,
#         tolerance: float = None,
#         space: om.MSpace = None
#     ) -> Tuple[om.MPoint, float, float]:
#
#         """
#         Intersecte un rayon avec la surface.
#
#         Args:
#             ray_start (om.MPoint):
#                 Point de départ du rayon.
#
#             ray_dir (om.MVector):
#                 Direction du rayon.
#
#             tolerance (float, optional):
#                 Tolérance de l'intersection.
#
#             space (om.MSpace, optional):
#                 Espace dans lequel effectuer l'intersection.
#
#         Returns
#             Tuple[om.MPoint, float, float]:
#                 Point d'intersection, paramètre U, paramètre V.
#         """
#
#         if tolerance is None:
#             tolerance = 1e-3
#
#         if space is None:
#             space = om.MSpace.kWorld
#
#         return self.mfnNurbsSurface.intersect(
#             ray_start,
#             ray_dir,
#             tolerance,
#             space
#         )
#
#     def is_param_on_surface(
#         self,
#         u: float,
#         v: float
#     ) -> bool:
#
#         """
#         Vérifie si un point est sur la surface.
#
#         Args:
#             u (float):
#                 Paramètre U du point à vérifier.
#
#             v (float):
#                 Paramètre V du point à vérifier.
#
#         Returns
#             bool:
#                 Si le point est sur la surface.
#         """
#
#         return self.mfnNurbsSurface.isParamOnSurface(u, v)
#
#     def is_point_on_trimmed_region(
#         self,
#         u: float,
#         v: float
#     ) -> bool:
#
#         """
#         Vérifie si un point est sur une région trimmée de la surface.
#
#         Args:
#             u (float):
#                 Paramètre U du point à vérifier.
#
#             v (float):
#                 Paramètre V du point à vérifier.
#
#         Returns
#             bool:
#                 Si le point est sur une région trimmée de la surface.
#         """
#
#         return self.mfnNurbsSurface.isPointOnTrimmedEdge(u, v)
#
#     def is_point_on_surface(
#         self,
#         point: om.MPoint,
#         tolerance: float = None,
#         space: om.MSpace = None
#     ) -> bool:
#
#         """
#         Vérifie si un point est sur la surface.
#
#         Args:
#             point (om.MPoint):
#                 Point à vérifier.
#
#             tolerance (float, optional):
#                 Tolérance de la vérification.
#
#             space (om.MSpace, optional):
#                 Espace dans lequel vérifier le point.
#
#         Returns
#             bool:
#                 Si le point est sur la surface.
#         """
#
#         if tolerance is None:
#             tolerance = 1e-3
#
#         if space is None:
#             space = om.MSpace.kWorld
#
#         return self.mfnNurbsSurface.isPointOnSurface(point, tolerance, space)
#
# # - CVs -----------------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def add_cvs(
#         self,
#         points: Union[
#             om.MPoint,
#             List[om.MPoint],
#             om.MPointArray,
#             List[Union[int, float]],
#             List[List[Union[int, float]]]]
#     ) -> None:
#
#         """
#         Ajoute des points à la surface.
#
#         Peut être une liste de MPoint, une liste de listes de float,
#         une MPointArray ou un MPoint.
#         Dans tous les cas, les points sont convertis en MPointArray,
#         puis ajoutés à la surface.
#
#         Parameters
#         ----------
#         points : Union[
#             om.MPoint,  # Un MPoint.
#             List[om.MPoint],  # Une liste de MPoint.
#             om.MPointArray,  # Une MPointArray.
#             List[Union[int, float]],  # Une liste de float et/ou int.
#             List[List[Union[int, float]]]]  # Une liste de listes
#                                             # de float et/ou int.
#
#             Points à ajouter à la surface.
#
#         Returns
#         -------
#         None
#         """
#
#         if not points:
#             return
#
#         for point in (
#             convert.to_mpointarray([om.MPoint(points)])
#             if isinstance(points, list) and len(points) == 3 else
#             convert.to_mpointarray([points])
#             if isinstance(points, om.MPoint) else
#             points
#         ):
#             self._cvs.append(point)
#
#     def add_line(
#         self,
#         start: om.MPoint = None,
#         end: om.MPoint = None,
#         line: Union[
#             om.MPointArray,
#             List[List[Union[int, float]]]] = None
#     ) -> None:
#
#         """
#         Ajoute une ligne à la surface.
#
#         Parameters
#         ----------
#         start : om.MPoint
#             Point de départ de la ligne.
#         end : om.MPoint
#             Point d'arrivée de la ligne.
#         line : Union[
#             om.MPointArray,
#             List[List[Union[int, float]]]
#
#         Returns
#         -------
#         None
#
#         Examples
#         --------
#         >>> surface = Surface()
#         >>> surface.add_line(
#         ...     start=om.MPoint(0, 0, 0),
#         ...     end=om.MPoint(1, 1, 1))
#         >>> surface.add_line(
#         ...     line=om.MPointArray([
#         ...         om.MPoint(0, 0, 0),
#         ...         om.MPoint(1, 1, 1)]))
#         >>> surface.add_line(
#         ...     line=[
#         ...         [0, 0, 0],
#         ...         [1, 1, 1]])
#         """
#
#         if start and end and not line:
#             self.add_cvs(start)
#             self.add_cvs(end)
#         elif line and not start and not end:
#             self.add_cvs(line)
#         else:
#             raise RuntimeError(
#                 "La ligne doit être définie par deux points.")
#
#     def remove_cvs(
#         self,
#         indices: Union[List[int], int]
#     ) -> None:
#
#         """
#         Supprime des points de la surface.
#
#         Parameters
#         ----------
#         indices : Union[List[int], int]
#             Indices des points à supprimer.
#
#         Returns
#         -------
#         None
#         """
#
#         if isinstance(indices, int):
#             indices = [indices]
#
#         for index in indices:
#             self._cvs.remove(index)
#
#     def clear_cvs(
#         self
#     ) -> None:
#
#         """
#         Supprime tous les points de la surface.
#
#         Parameters
#         ----------
#         None
#
#         Returns
#         -------
#         None
#         """
#
#         self._cvs.clear()
#
#     def cv(self, uIndex: int, vIndex: int) -> om.MObject:
#
#         """
#         Récupère le CV de la surface aux indices donnés.
#
#         Args:
#             uIndex : int, Index U du CV à récupérer.
#             vIndex : int, Index V du CV à récupérer.
#
#         Returns:
#             om.MObject: CV de la surface aux indices donnés.
#         """
#
#         return self.mfnNurbsSurface.cv(uIndex, vIndex)
#
#     def get_cv_position(
#         self,
#         uIndex: int,
#         vIndex: int,
#         space: Optional[om.MSpace] = None
#     ) -> om.MPoint:
#
#         """
#         Récupère la position du CV de la surface aux indices donnés.
#
#         Args:
#             uIndex : int
#                 Index U du CV à récupérer.
#             vIndex : int
#                 Index V du CV à récupérer.
#             space : Optional[om.MSpace], optional
#                 Espace dans lequel récupérer la position du CV.
#
#         Returns
#             om.MPoint
#                 Position du CV de la surface aux indices donnés.
#         """
#
#         if space is None:
#             space = om.MSpace.kObject
#
#         return self.mfnNurbsSurface.cvPosition(uIndex, vIndex, space)
#
#     def get_cvs(
#         self,
#         space: Optional[Union[om.MSpace, int]] = None
#     ) -> om.MPointArray:
#
#         """
#         Récupère les positions des CVs de la surface.
#
#         Args:
#             space (Optional[Union[om.MSpace, int]], optional):
#                 Espace dans lequel récupérer les positions des CVs.
#
#         Returns
#             om.MPointArray
#                 Positions des CVs de la surface.
#         """
#
#         if not self.exists:
#             return self._cvs
#
#         if space is None:
#             space = om.MSpace.kObject
#
#         return self.mfnNurbsSurface.cvPositions(space=space)
#
#     def set_cv_position(
#         self,
#         uIndex: int,
#         vIndex: int,
#         position: om.MPoint,
#         space: Optional[om.MSpace] = None
#     ) -> None:
#
#         """
#         Définit la position du CV de la surface aux indices donnés.
#
#         Args:
#             uIndex : int
#                 Index U du CV à définir.
#
#             vIndex : int
#                 Index V du CV à définir.
#
#             position : om.MPoint
#                 Position du CV à définir.
#
#             space : Optional[om.MSpace], optional
#                 Espace dans lequel définir la position du CV.
#
#         Returns
#             None
#         """
#
#         if space is None:
#             space = om.MSpace.kObject
#
#         self.mfnNurbsSurface.setCVPosition(uIndex, vIndex, position, space)
#
#     def set_cv_positions(
#         self,
#         positions: om.MPointArray,
#         space: om.MSpace = om.MSpace.kWorld
#     ) -> None:
#
#         """
#         Définit les positions des CVs de la surface.
#
#         Parameters
#         ----------
#         positions : om.MPointArray
#             Positions des CVs à définir.
#
#         space : om.MSpace
#             Espace dans lequel définir les positions des CVs.
#
#         Returns
#         -------
#             None
#         """
#
#         surface_fn = om.MFnNurbsSurface(self.maya_dagPath)
#         mfnNurbsSurface.setCVPositions(positions, space)
#         mfnNurbsSurface.updateSurface()
#
#     def cvs_in_u(
#         self,
#         startUIndex: int = 0,
#         endUIndex: int = -1,
#         vIndex: int = 0
#     ) -> om.MObject:
#
#         """
#         Récupère les CVs de la surface entre les indices U donnés.
#
#         Parameters
#         ----------
#         startUIndex : int
#             Index U de début de récupération des CVs.
#         endUIndex : int
#             Index U de fin de récupération des CVs.
#         vIndex : int
#             Index V des CVs à récupérer.
#
#         Returns
#         -------
#         om.MObject
#             CVs de la surface entre les indices U donnés.
#         """
#
#         return self.mfnNurbsSurface.cvsInU(startUIndex, endUIndex, vIndex)
#
#     def cvs_in_v(
#         self,
#         startVIndex: int = 0,
#         endVIndex: int = -1,
#         uIndex: int = 0
#     ) -> om.MObject:
#
#         """
#         Récupère les CVs de la surface entre les indices V donnés.
#
#         Parameters
#         ----------
#         startVIndex : int
#             Index V de début de récupération des CVs.
#         endVIndex : int
#             Index V de fin de récupération des CVs.
#         uIndex : int
#             Index U des CVs à récupérer.
#
#         Returns
#         -------
#         om.MObject
#             CVs de la surface entre les indices V donnés.
#         """
#
#         return self.mfnNurbsSurface.cvsInV(startVIndex, endVIndex, uIndex)
#
# # - Knots ---------------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def add_u_knots(
#         self,
#         knots: Union[List[Union[int, float]], int]
#     ) -> None:
#
#         """
#         Ajoute des noeuds U à la surface.
#
#         Parameters
#         ----------
#         knots : Union[List[Union[int, float]], int]
#             Noeuds U à ajouter.
#
#         Returns
#         -------
#         None
#         """
#
#         self._add_knots(
#             knots=knots,
#             knots_list=self._u_knots
#         )
#
#     def add_v_knots(
#         self,
#         knots: Union[List[Union[int, float]], int]
#     ) -> None:
#
#         """
#         Ajoute des noeuds V à la surface.
#
#         Parameters
#         ----------
#         knots : Union[List[Union[int, float]], int]
#             Noeuds V à ajouter.
#
#         Returns
#         -------
#         None
#         """
#
#         self._add_knots(
#             knots=knots,
#             knots_list=self._v_knots
#         )
#
#     def remove_u_knots(
#         self,
#         indices: Union[List[int], int],
#     ) -> None:
#
#         """
#         Supprime des noeuds U de la surface.
#
#         Parameters
#         ----------
#         indices : Union[List[int], int]
#             Noeuds U à supprimer.
#
#         Returns
#         -------
#         None
#         """
#
#         self._remove_knots(
#             indices,
#             knots_list=self._u_knots
#         )
#
#     def remove_v_knots(
#         self,
#         indices: Union[List[int], int],
#     ) -> None:
#
#         """
#         Supprime des noeuds V de la surface.
#
#         Parameters
#         ----------
#         indices : Union[List[int], int]
#             Noeuds V à supprimer.
#
#         Returns
#         -------
#         None
#         """
#
#         self._remove_knots(
#             indices=indices,
#             knots_list=self._v_knots
#         )
#
#     def clear_knots(
#         self
#     ) -> None:
#
#         """
#         Supprime tous les noeuds de la surface.
#
#         Parameters
#         ----------
#         None
#
#         Returns
#         -------
#         None
#         """
#
#         self.u_knots.clear()
#         self.v_knots.clear()
#
#     def clear_u_knots(
#         self
#     ) -> None:
#
#         """
#         Supprime tous les noeuds U de la surface.
#
#         Parameters
#         ----------
#         None
#
#         Returns
#         -------
#         None
#         """
#
#         self._u_knots.clear()
#
#     def clear_v_knots(
#         self
#     ) -> None:
#
#         """
#         Supprime tous les noeuds V de la surface.
#
#         Parameters
#         ----------
#         None
#
#         Returns
#         -------
#         None
#         """
#
#         self._v_knots.clear()
#
#     def set_u_knot(
#         self,
#         index: int,
#         knot: int
#     ) -> None:
#
#         """
#         Modifie un noeud U de la surface.
#
#         Parameters
#         ----------
#         index : int
#             Index du noeud U à modifier.
#         knot : int
#             Nouvelle valeur du noeud U.
#
#         Returns
#         -------
#         None
#         """
#
#         self._u_knots[index] = knot
#
#     def set_v_knot(
#         self,
#         index: int,
#         knot: int
#     ) -> None:
#
#         """
#         Modifie un noeud V de la surface.
#
#         Parameters
#         ----------
#         index : int
#             Index du noeud V à modifier.
#         knot : int
#             Nouvelle valeur du noeud V.
#
#         Returns
#         -------
#         None
#         """
#
#         self._v_knots[index] = knot
#
#     def get_u_knots(
#         self
#     ) -> List[float]:
#
#         """
#         Récupère les noeuds U de la surface.
#
#         Parameters
#         ----------
#         None
#
#         Returns
#         -------
#         List[float]
#             Noeuds U de la surface.
#         """
#
#         return (
#             self.mfnNurbsSurface.knotsInU()
#             if self.exists
#             else None
#         )
#
#     def get_v_knots(
#         self
#     ) -> List[float]:
#
#         """
#         Récupère les noeuds V de la surface.
#
#         Parameters
#         ----------
#         None
#
#         Returns
#         -------
#         List[float]
#             Noeuds V de la surface.
#         """
#
#         return (
#             self.mfnNurbsSurface.knotsInV()
#             if self.exists
#             else None
#         )
#
# # - Degrees -------------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def set_u_degree(
#         self,
#         degree: int
#     ) -> None:
#
#         """
#         Modifie le degré U de la surface.
#
#         Parameters
#         ----------
#         degree : int
#             Nouvelle valeur du degré U.
#
#         Returns
#         -------
#         None
#         """
#
#         self._u_degree = degree
#         self.cvs = self._generate_cvs()
#         self._update_knots()
#
#     def set_v_degree(
#         self,
#         degree: int
#     ) -> None:
#
#         """
#         Modifie le degré V de la surface.
#
#         Parameters
#         ----------
#         degree : int
#             Nouvelle valeur du degré V.
#
#         Returns
#         -------
#         None
#         """
#
#         self._v_degree = degree
#         self.cvs = self._generate_cvs()
#         self._update_knots()
#
#     def set_degrees(
#         self,
#         degrees: Union[List[int], int]
#     ) -> None:
#
#         """
#         Modifie les degrés de la surface.
#         Si un seul degré est donné, les deux degrés seront modifiés
#         avec cette même valeur.
#         Si deux degrés sont donnés, le premier sera le degré U
#         et le second sera le degré V.
#
#         Parameters
#         ----------
#         degrees : Union[List[int], int]
#             Nouvelles valeurs des degrés.
#
#         Returns
#         -------
#         None
#         """
#
#         if isinstance(degrees, int):
#             degrees = [degrees, degrees]
#
#         self.set_u_degree(degrees[0])
#         self.set_v_degree(degrees[1])
#
#     def get_u_degree(
#         self
#     ) -> int:
#
#         """
#         Récupère le degré U de la surface.
#
#         Parameters
#         ----------
#         None
#
#         Returns
#         -------
#         int
#             Degré U de la surface.
#         """
#
#         return (
#             self.mfnNurbsSurface.degreeInU
#             if self.exists
#             else (
#                 self._u_degree
#                 if hasattr(self, "_u_degree")
#                 else 0
#             )
#         )
#
#     def get_v_degree(
#         self
#     ) -> int:
#
#         """
#         Récupère le degré V de la surface.
#
#         Parameters
#         ----------
#         None
#
#         Returns
#         -------
#         int
#             Degré V de la surface.
#         """
#
#         return (
#             self.mfnNurbsSurface.degreeInV
#             if self.exists
#             else (
#                 self._v_degree
#                 if hasattr(self, "_v_degree")
#                 else 0
#             )
#         )
#
# # - Spans ---------------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def set_u_spans(
#         self,
#         spans: Union[List[int], int]
#     ) -> None:
#
#         """
#         Modifie les spans U de la surface.
#
#         Parameters
#         ----------
#         spans : Union[List[int], int]
#             Nouvelles valeurs des spans U.
#
#         Returns
#         -------
#         None
#         """
#
#         self._u_spans = spans
#         self.cvs = self._generate_cvs()
#         self._update_knots()
#
#     def set_v_spans(
#         self,
#         spans: Union[List[int], int]
#     ) -> None:
#
#         """
#         Modifie les spans V de la surface.
#
#         Parameters
#         ----------
#         spans : Union[List[int], int]
#             Nouvelles valeurs des spans V.
#
#         Returns
#         -------
#         None
#         """
#
#         self._v_spans = spans
#         self._update_knots()
#         self.cvs = self._generate_cvs()
#
#     def get_u_spans(
#         self
#     ) -> int:
#
#         """
#         Récupère les spans U de la surface existante.
#
#         Parameters
#         ----------
#         None
#
#         Returns
#         -------
#         int
#             Spans U de la surface.
#         """
#
#         return (
#             self.mfnNurbsSurface.numSpansInU
#             if self.exists
#             else (
#                 self._u_spans
#                 if hasattr(self, "_u_spans")
#                 else 0
#             )
#         )
#
#     def get_v_spans(
#         self
#     ) -> int:
#
#         """
#         Récupère les spans V de la surface existante.
#
#         Parameters
#         ----------
#         None
#
#         Returns
#         -------
#         int
#             Spans V de la surface.
#         """
#
#         return (
#             self.mfnNurbsSurface.numSpansInV
#             if self.exists
#             else 0
#         )
#
# # - Form ----------------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def get_v_form(
#         self
#     ) -> int:
#
#         """
#         Retourne la forme V de la surface.
#
#         Returns
#         -------
#         int
#             La forme V de la surface.
#             0 = Invalide
#             1 = Open
#             2 = Closed
#             3 = Periodic
#         """
#
#         return (
#             self.mfnNurbsSurface.formInV
#             if self.exists
#             else None
#         )
#
#     def get_u_form(
#         self
#     ) -> int:
#
#         """
#         Retourne la forme U de la surface.
#
#         Returns
#         -------
#         int
#             La forme U de la surface.
#             0 = Invalide
#             1 = Open
#             2 = Closed
#             3 = Periodic
#         """
#
#         return (
#             self.mfnNurbsSurface.formInU
#             if self.exists
#             else None
#         )
#
# # -----------------------------------------------------------------------------
# # PRIVATE FUNCTIONS -----------------------------------------------------------
# # - Init ----------------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def _init_surface_properties(
#         self
#     ) -> None:
#
#         """
#         Initialise les propriétés de la surface.
#
#         Parameters
#         ----------
#         None
#
#         Returns
#         -------
#         None
#         """
#
#         self._shape_orig_type = type(self)
#         self._surface_fn = (
#             om.MFnNurbsSurface(self.maya_dagPath)
#             if self.maya_dagPath is not None
#             else om.MFnNurbsSurface()
#         )
#         self._init_form()
#
# # - Attributes ----------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def _set_surface_attribute(
#         self,
#         axis: str,
#         attribute: str,
#         value: int,
#         method: Callable
#     ) -> None:
#
#         """
#         Fonction privée qui définit un attribut de la surface.
#
#         Args:
#             axis (str):
#                 L'axe de l'attribut à définir, soit 'u' ou 'v'.
#
#             attribute (str):
#                 L'attribut à définir.
#
#             value (int):
#                 La valeur à donner à l'attribut.
#
#             method (function):
#                 La méthode à utiliser pour définir l'attribut.
#
#         Returns:
#             None
#         """
#
#         attr_name = f"_{axis}_{attribute}"
#         had_orig = False
#         shape_orig = self.shape_orig
#
#         if not self.exists:
#             method(value)
#             setattr(shape_orig, attr_name, value)
#             return
#
#         if shape_orig.exists:
#             orig_incoming_connections = shape_orig.incoming_connections
#             orig_outgoing_connections = shape_orig.outgoing_connections
#             had_orig = True
#             shape_orig.delete()
#
#         incoming_connections = self.incoming_connections
#         outgoing_connections = self.outgoing_connections
#
#         self.delete()
#         setattr(self, attr_name, value)
#         method(value)
#         setattr(shape_orig, attr_name, value)
#         getattr(shape_orig, method.__name__)(value)
#
#         self.create(
#             incoming_connections,
#             outgoing_connections
#         )
#
#         if had_orig:
#             shape_orig.create(
#                 orig_incoming_connections,
#                 orig_outgoing_connections
#             )
#
# # - Converters ----------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def _int_to_space(
#         self,
#         space: int
#     ) -> int:
#
#         """
#         Retourne l'espace de la surface.
#
#         Parameters
#         ----------
#         space : int
#             Espace de la surface.
#
#         Returns
#         -------
#         int
#             Espace de la surface.
#         """
#
#         if space == 0:
#             return om.MSpace.kInvalid
#         elif space == 1:
#             return om.MSpace.kTransform
#         elif space == 2:
#             return om.MSpace.kObject
#         elif space == 3:
#             return om.MSpace.kPostTransform
#         elif space == 4:
#             return om.MSpace.kWorld
#         elif space == 5:
#             return om.MSpace.kLast
#
# # - Form ----------------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def _default_form(
#         self
#     ) -> None:
#
#         """
#         Définit la forme par défaut de la surface.
#
#         Parameters
#         ----------
#         None
#
#         Returns
#         -------
#         None
#         """
#
#         self._cvs = [
#             om.MPoint(-1, 0, 1, 1),
#             om.MPoint(-1, 0, -1, 1),
#             om.MPoint(1, 0, 1, 1),
#             om.MPoint(1, 0, -1, 1)
#         ]
#         self._u_degree = 1
#         self._v_degree = 1
#         self._u_spans = 1
#         self._v_spans = 1
#         self._u_knots = self._generate_knots(
#             self._u_degree,
#             self._u_spans
#         )
#         self._v_knots = self._generate_knots(
#             self._v_degree,
#             self._v_spans
#         )
#         self._u_form = 1
#         self._v_form = 1
#         self._is_uniform = False
#         self._is_rational = True
#
#     def _user_form(
#         self
#     ) -> None:
#
#         """
#         Définit la forme de la surface selon le nom de la surface
#         fourni par l'utilisateur.
#
#         Returns
#             None
#         """
#
#         self._cvs = om.MFnNurbsSurface(self.maya_dagPath).cvPositions()
#         self._u_degree = self.get_u_degree()
#         self._v_degree = self.get_v_degree()
#         self._u_spans = self.get_u_spans()
#         self._v_spans = self.get_v_spans()
#         self._u_knots = self.get_u_knots()
#         self._v_knots = self.get_v_knots()
#         self._u_form = self.get_u_form()
#         self._v_form = self.get_v_form()
#         self._is_uniform = self._get_is_uniform()
#         self._is_rational = self._get_is_rational()
#
#         if (orig := self.shape_orig) is not None:
#             orig._cvs = om.MFnNurbsSurface(self.maya_dagPath).cvPositions()
#             orig._u_degree = self.get_u_degree()
#             orig._v_degree = self.get_v_degree()
#             orig._u_spans = self.get_u_spans()
#             orig._v_spans = self.get_v_spans()
#             orig._u_knots = self.get_u_knots()
#             orig._v_knots = self.get_v_knots()
#             orig._u_form = self.get_u_form()
#             orig._v_form = self.get_v_form()
#             orig._is_uniform = self._get_is_uniform()
#             orig._is_rational = self._get_is_rational()
#
#     def _init_form(
#         self
#     ) -> None:
#
#         """
#         Initialise la forme de la surface.
#         Si la surface n'existe pas, la forme par défaut est utilisée.
#         Sinon, la forme de la surface est définie selon le nom de la surface
#         fourni par l'utilisateur.
#
#         Parameters
#         ----------
#         name : str = None
#             Nom de la surface.
#
#         Returns
#         -------
#         None
#         """
#
#         if not self.exists:
#             self._default_form()
#         else:
#             self._user_form()
#
# # - CVs -----------------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def _generate_cvs(
#         self,
#         u_spans: Optional[int] = None,
#         v_spans: Optional[int] = None,
#         u_degree: Optional[int] = None,
#         v_degree: Optional[int] = None
#     ) -> List[List[float]]:
#
#         """
#         Génère une list de CVs selon le nombre de
#         spans et le degré de la surface.
#
#         Parameters
#         ----------
#         u_spans : Optional[int]
#             Nombre de spans en U.
#         v_spans : Optional[int]
#             Nombre de spans en V.
#         u_degree : Optional[int]
#             Degré en U.
#         v_degree : Optional[int]
#             Degré en V.
#
#         Returns
#         -------
#         List[List[float]]
#         """
#
#         if not u_degree:
#             u_degree = self._u_degree
#         if not u_spans:
#             u_spans = self._u_spans
#         if not v_degree:
#             v_degree = self._v_degree
#         if not v_spans:
#             v_spans = self._v_spans
#
#         cvs = []
#         for u in range(u_spans + u_degree):
#             for v in range(v_spans + v_degree):
#                 u_pos = u
#                 v_pos = v
#                 if u_degree > 1:
#                     if u == 1:
#                         u_pos -= .5
#                     if u > 1:
#                         u_pos -= 1
#
#                 if v_degree > 1:
#                     if v == 1:
#                         v_pos -= .5
#                     if v > 1:
#                         v_pos -= 1
#
#                 if u_degree > 2:
#                     if u == u_degree + u_spans - 1:
#                         u_pos -= .5
#                     if u == u_degree + u_spans:
#                         u_pos -= 1.5
#
#                 if v_degree > 2:
#                     if v == v_degree + v_spans - 2:
#                         v_pos -= .5
#                     if v == v_degree + v_spans - 1:
#                         v_pos -= 1
#
#                 cvs.append([v_pos, 0, u_pos])
#
#         return cvs
#
# # - Knots ---------------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def _add_knots(
#         self,
#         knots: Union[List[Union[int, float]], int],
#         knots_list: List[Union[int, float]]
#     ) -> None:
#
#         """
#         Ajoute des noeuds à la surface.
#
#         Parameters
#         ----------
#         knots : Union[List[Union[int, float]], int]
#             Noeuds à ajouter.
#         knots_list : List[Union[int, float]]
#             Liste de noeuds de la surface.
#
#         Returns
#         -------
#         None
#         """
#
#         (
#             knots_list.extend(knots)
#             if (
#                 isinstance(knots, List)
#                 and all(
#                     isinstance(knot, (int, float))
#                     for knot in knots)
#             )
#             else (
#                 knots_list.append(knots)
#             )
#         )
#
#     def _remove_knots(
#         self,
#         indices: Union[List[int], int],
#         knots_list: List[Union[int, float]]
#     ) -> None:
#
#         """
#         Retire des noeuds à la surface.
#
#         Parameters
#         ----------
#         indices : Union[List[int], int]
#             Indices des noeuds à retirer.
#
#         knots_list : List[Union[int, float]]
#             Liste de noeuds de la surface.
#
#         Returns
#         -------
#         None
#         """
#
#         (
#             knots_list.pop(indices)
#             if isinstance(indices, int)
#             else (
#                 [
#                     knots_list.pop(index)
#                     for index in sorted(indices, reverse=True)
#                 ]
#             )
#         )
#
#     def _generate_knots(
#         self,
#         _spans: int,
#         _degree: int
#     ) -> List[float]:
#
#         """
#         Retourne les noeuds U de la surface par rapport au degré U et
#         au nombre de noeuds U.
#
#         Parameters
#         ----------
#         _spans : int
#             Nombre de noeuds dans la direction souhaitée.
#
#         _degree : int
#             Degree de la surface dans la direction souhaitée.
#
#         Returns
#         -------
#         List[float]
#             Noeuds U de la surface.
#         """
#
#         knots = [
#                 i / _spans
#                 for i in range(_spans + 1)
#         ]
#
#         if _degree == 2:
#             knots = [
#                 0.0,
#                 *knots,
#                 1.0
#             ]
#
#         elif _degree == 3:
#             knots = [
#                 0.0, 0.0,
#                 *knots,
#                 1.0, 1.0
#             ]
#
#         elif _degree == 5:
#             knots = [
#                 0.0, 0.0, 0.0, 0.0, 0.0,
#                 *knots,
#                 1.0, 1.0, 1.0, 1.0, 1.0, 1.0
#             ]
#
#         elif _degree == 8:
#             knots = [
#                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
#                 *knots,
#                 1.0, 1.0, 1.0, 1.0, 1.0, 1.0
#             ]
#
#         return knots
#
#     def _update_knots(
#         self
#     ) -> None:
#
#         """
#         Met à jour les noeuds de la surface en fonction des degrés et
#         des spans.
#
#         Parameters
#         ----------
#         None
#
#         Returns
#         -------
#         None
#         """
#
#         self.u_knots = convert.to_MDoubleArray(
#             self._generate_knots(
#                 self._u_spans,
#                 self._u_degree
#             )
#         )
#
#         self.v_knots = convert.to_MDoubleArray(
#             self._generate_knots(
#                 self._v_spans,
#                 self._v_degree
#             )
#         )
#
# # - Data ----------------------------------------------------------------------
# # -----------------------------------------------------------------------------
#     def _get_is_uniform(
#         self
#     ) -> bool:
#
#         """
#         Retourne si la surface est uniforme.
#
#         Parameters
#         ----------
#         None
#
#         Returns
#         -------
#         bool
#             Si la surface est uniforme.
#         """
#
#         return self.mfnNurbsSurface.isUniform if self.exists else None
#
#     def _get_is_rational(
#         self
#     ) -> bool:
#
#         """
#         Retourne si la surface est rationnelle.
#
#         Parameters
#         ----------
#         None
#
#         Returns
#         -------
#         bool
#             Si la surface est rationnelle.
#         """
#
#         if self.is_uniform:
#             return False
#
#         unique_positions = set()
#
#         for cv in self.cvs:
#             position = (cv.x, cv.y, cv.z)
#             unique_positions.add(position)
#
#         return len(unique_positions) > 1


NodeRegistry()[Surface.nodeType()] = Surface
