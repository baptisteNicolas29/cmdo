from typing import List, Union, Optional, Sequence, Dict, Any

import math

from maya import cmds
from maya.api import OpenMaya as om

from ...core import cmdoTyping as cmdoT
from ...core.nodeRegistry import NodeRegistry
from ...core.abstract import dagLib


class Curve(dagLib.DAGNode):

    _NODE_TYPE = "nurbsCurve"
    _API_TYPE = om.MFn.kNurbsCurve

    @property
    def mfnNurbsCurve(self) -> om.MFnNurbsCurve:

        """
        Get MFnNurbsCurve of the om.MObject

        :return:
            om.MFnNurbsCurve: the curve object
        """

        return om.MFnNurbsCurve(self)

    @property
    def cvs(self) -> om.MPointArray:

        """
        Get curve control vertices positions

        :return: om.MPointArray: Les CVs de la curve.
        """

        return self.mfnNurbsCurve.cvPositions()

    @cvs.setter
    def cvs(self, points: Union[om.MPointArray, cmdoT.CmdoList]) -> None:

        """
        Define curve cvs

        :param points: om.MPointArray, Les CVs de la curve.

        """

        points = om.MPointArray(list(points))

        self.mfnNurbsCurve.setCVPositions(points)
        self.mfnNurbsCurve.updateCurve()

    @property
    def cvCount(self) -> int:

        """
        Get the number of cvs

        :return: int, the number of cvs
        """

        return len(self.cvs) or 0

    @property
    def degree(self) -> int:

        """
        Get the curve degree

        :return: int, the curve degree
        """

        return self.mfnNurbsCurve.degree

    @degree.setter
    def degree(self, degree: int) -> None:

        """
        Set the curve degree

        :param degree: int, the curve degree to set

        """

        self.mfnNurbsCurve.degree = degree
        self.mfnNurbsCurve.updateCurve()

    @property
    def knots(self) -> om.MDoubleArray:

        """
        Get curve knots -> numberOfPoints + degree - 1

        :return: om.MDoubleArray, the curve knots
        """

        return self.mfnNurbsCurve.knots()

    @knots.setter
    def knots(self, knots: Union[om.MDoubleArray, cmdoT.CmdoList]) -> None:

        """
        Set the curve knots

        :param knots: om.MDoubleArray, the curve knots to set

        """
        knots = om.MDoubleArray(list(knots))

        self.mfnNurbsCurve.setKnots(knots)
        self.mfnNurbsCurve.updateCurve()

    @property
    def form(self) -> int:

        """
        Get the form of the curve

        :return: int: the form of the curve
        """

        return self.mfnNurbsCurve.form

    @form.setter
    def form(self, form: int) -> None:

        """
        Set the curve form
            0 = Invalid
            1 = Open
            2 = Closed
            3 = Periodic

        :param form: int, the form of the curve to set

        """

        self.mfnNurbsCurve.form = form

    @property
    def isRational(self) -> bool:

        """
        Is the curve rational

        :return: bool, is the curve rational
        """

        return any(weight != 1.0 for weight in self.knots)

    @property
    def lineWidth(self) -> float:

        """
        Get the lineWidth of the curve

        :return: float, the width of the curve
        """

        return self['lineWidth'].asFloat()

    @lineWidth.setter
    def lineWidth(self, width: float) -> None:

        """
        Set the form of the curve

        :param width: float, the form of the curve to set

        """

        self['lineWidth'] = width

    def update(self) -> None:

        """
        Update the curve

        """

        self.mfnNurbsCurve.updateCurve()

    def translate(self, vector: List[Union[float, int]]) -> None:

        """
        Translate the curve

        :param vector: list[float|int], the translation value

        """

        if isinstance(vector, (float, int)):
            vector = [vector, vector, vector]

        for index in range(self.cvCount):
            point = om.MPoint(*[self.cvs[index][i]+vector[i] for i in range(3)])
            self.mfnNurbsCurve.setCVPosition(index, point, om.MSpace.kObject)

        self.update()

    def rotate(self, rotation: List[Union[float, int]]) -> None:

        """
        Rotate the curve

        :param rotation: List[Union[float, int]], the rotation value

        """

        if isinstance(rotation, (float, int)):
            rotation = [rotation, rotation, rotation]

        for index in range(self.cvCount):
            vector = om.MVector(*[self.cvs[index][i] for i in range(3)])

            point = vector.rotateBy(
                om.MEulerRotation(
                    math.radians(rotation[0]),
                    math.radians(rotation[1]),
                    math.radians(rotation[2])
                )
            )

            self.mfnNurbsCurve.setCVPosition(index, point, om.MSpace.kObject)

        self.update()

    def scale(self, vector: List[Union[float, int]]) -> None:

        """
        Scale the curve

        :param vector: List[float, int], the scale value

        """

        if isinstance(vector, (float, int)):
            vector = [vector, vector, vector]

        for index in range(self.cvCount):
            point = om.MPoint(*[self.cvs[index][i]*vector[i] for i in range(3)])
            self.mfnNurbsCurve.setCVPosition(index, point, om.MSpace.kObject)

        self.update()

    def setCVPositions(self, pointList: Union[om.MPointArray, cmdoT.CmdoList], space: int = om.MSpace.kObject) -> None:

        """
        Set all cv positions

        :param pointList: List[List[int, float]], the new cv positions
        :param space: int, the space in which to set the cvs

        """

        mPointArray = om.MPointArray(pointList)
        self.mfnNurbsCurve.setCVPositions(mPointArray, space)
        self.update()

    def getClosestPoint(self, point, **kwargs):
        """
        Get the closest point on current curve given a point to test

        :param point: the point to get the closest point for
        :param kwargs: accepted kwargs are:
            guess<float>,
            tolerance<float>,
            space<om.MSpace>

        :return: om.MPoint, the closest point on curve from given point
        """

        if not isinstance(point, om.MPoint) and len(point) == 3:
            point = om.MPoint(*point)

        return self.mfnNurbsCurve.closestPoint(point, **kwargs)

# - Export --------------------------------------------------------------------
# -----------------------------------------------------------------------------
#     def export_form(
#         self,
#         name: str
#     ) -> str:
#
#         """
#         Exporte la curve.
#
#         Args:
#             name (str):
#                 Le nom du fichier.
#
#         Returns
#             str
#                 Le chemin du fichier.
#         """
#
#         exportLib.export_dict_to_json(
#             self._get_dict_form(),
#             name,
#             path=self.export_path,
#             )
#         return self.export_path
#
#     def import_form(
#         self,
#         name: str
#     ) -> None:
#
#         """
#         Importe la curve.
#
#         Args:
#             name (str):
#                 Le nom du fichier.
#
#         Returns
#             None
#         """
#
#         exists = False
#         if self.exists:
#             exists = True
#             self.delete()
#
#         data = exportLib.import_dict_from_json(
#             name=name,
#             path=self.export_path)
#
#         self.cvs = convert.to_mpointarray(data["cvs"])
#         self.knots = convert.to_MDoubleArray(data["knots"])
#         self.degree = data["degree"]
#         self.form = data["form"]
#         self.is_2d = data["is_2d"]
#         self.is_rational = data["is_rational"]
#
#         if exists:
#             self.create()

    # def _default_form(self) -> None:
    #
    #     """
    #     Définit la forme par défaut de la curve.
    #
    #     Parameters
    #     ----------
    #     None
    #
    #     Returns
    #     -------
    #     None
    #     """
    #
    #     self.cvs = om.MPointArray(
    #         [om.MPoint(0, 0, 0), om.MPoint(0, 1, 0)]
    #     )
    #     self._degree = 1
    #     self._knots = self._generate_knots(len(self.cvs), self._degree)
    #     self._form = 1
    #     self._is_2d = False
    #     self._is_rational = True
    #
    # def _user_form(self) -> None:
    #
    #     """
    #     Définit la forme de la curve selon le nom de la curve
    #     fourni par l'utilisateur.
    #
    #     Returns
    #     -------
    #     None
    #     """
    #
    #     self._degree = self.mfnNurbsCurve.degree
    #     self._knots = self.mfnNurbsCurve.knots()
    #     self._form = self.mfnNurbsCurve.form
    #     self._is_2d = False
    #     self._is_rational = self._get_is_rational()
    #
    # def _get_dict_form(
    #     self
    # ) -> Dict[str, Any]:
    #
    #     """
    #     Récupère les informations de la forme de la curve.
    #
    #     Returns
    #         Dict[str, Any]:
    #             Informations de la forme de la curve.
    #     """
    #
    #     return {
    #         "degree": self.degree,
    #         "form": self.form,
    #         "is_2d": self.is_2d,
    #         "is_rational": self.is_rational,
    #         "knots": listself.knots),
    #         "cvs": list(self.cvs)
    #     }
    #
    # def _generate_knots(self, num_cvs: int, degree: int) -> List[float]:
    #
    #     """
    #     Génère les valeurs des knots de la curve.
    #
    #     Args :
    #         num_cvs (int) :
    #             Nombre de cvs de la curve.
    #         degree (int) :
    #             Degré de la curve.
    #
    #     :return:
    #         List[float] : Valeurs des knots de la curve.
    #     """
    #
    #     len_knots = num_cvs + degree - 1
    #     return [i/(len_knots-1) for i in range(len_knots)]


NodeRegistry()[Curve.nodeType()] = Curve

