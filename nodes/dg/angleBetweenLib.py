from typing import List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class AngleBetween(dgLib.DGNode):

    _NODE_TYPE = "angleBetween"
    _API_TYPE = om.MFn.kAngleBetween

    @property
    def vector1(self) -> List[float]:

        """
        Get the vector1 value

        :return: List[float], the vector1 value
        """

        return self['vector1'].value

    @vector1.setter
    def vector1(self, value: Union[List[float], om.MPlug]) -> None:

        """
        Set the vector1 value

        :param value: List[float], the vector1 value
        """

        self['vector1'] = value

    @property
    def vector1X(self) -> float:

        """
        Get the vector1X value

        :return: float, the vector1X value
        """

        return self['vector1X'].asFloat()

    @vector1X.setter
    def vector1X(self, value: Union[float, om.MPlug]) -> None:

        """
        Set the vector1X value

        :param value: float, the vector1X value
        """

        self['vector1X'] = value

    @property
    def vector1Y(self) -> float:

        """
        Get the vector1Y value

        :return: float, the vector1Y value
        """

        return self['vector1Y'].asFloat()

    @vector1Y.setter
    def vector1Y(self, value: Union[float, om.MPlug]) -> None:

        """
        Set the vector1Y value

        :param value: float, the vector1Y value
        """

        self['vector1Y'] = value

    @property
    def vector1Z(self) -> float:

        """
        Get the vector1Z value

        :return: float, the vector1Z value
        """

        return self['vector1Z'].asFloat()

    @vector1Z.setter
    def vector1Z(self, value: Union[float, om.MPlug]) -> None:

        """
        Set the vector1Z value

        :param value: float, the vector1Z value
        """

        self['vector1Z'] = value

    @property
    def vector2(self) -> List[float]:

        """
        Get the vector2 value

        :return: List[float], the vector2 value
        """

        return self['vector2'].value

    @vector2.setter
    def vector2(self, value: List[float]) -> None:

        """
        Set the vector2 value

        :param value: List[float], the vector2 value
        """

        self['vector2'] = value

    @property
    def vector2X(self) -> float:

        """
        Get the vector2X value

        :return: float, the vector2X value
        """

        return self['vector2X'].asFloat()

    @vector2X.setter
    def vector2X(self, value: Union[float, om.MPlug]) -> None:

        """
        Set the vector2X value

        :param value: float, the vector2X value
        """

        self['vector2X'] = value

    @property
    def vector2Y(self) -> float:

        """
        Get the vector2Y value

        :return: float, the vector2Y value
        """

        return self['vector2Y'].asFloat()

    @vector2Y.setter
    def vector2Y(self, value: Union[float, om.MPlug]) -> None:

        """
        Set the vector2Y value

        :param value: float, the vector2Y value
        """

        self['vector2Y'] = value

    @property
    def vector2Z(self) -> float:

        """
        Get the vector2Z value

        :return: float, the vector2Z value
        """

        return self['vector2Z'].asFloat()

    @vector2Z.setter
    def vector2Z(self, value: Union[float, om.MPlug]) -> None:

        """
        Set the vector2Z value

        :param value: float, the vector2Z value
        """

        self['vector2Z'] = value

    @property
    def euler(self) -> List[float]:

        """
        Get euler value

        :return: List[float], the euler value
        """

        return self['euler'].value

    @property
    def eulerX(self) -> float:

        """
        Get eulerX value

        :return: List[float], the eulerX value
        """

        return self['eulerX'].value

    @property
    def eulerY(self) -> float:

        """
        Get eulerY value

        :return: List[float], the eulerY value
        """

        return self['eulerY'].value

    @property
    def eulerZ(self) -> float:

        """
        Get eulerZ value

        :return: List[float], the eulerZ value
        """

        return self['eulerZ'].value

    @property
    def angle(self) -> float:

        """
        Get the angle value

        :return: float, the angle value
        """

        return self['angle'].value

    @property
    def axis(self) -> List[float]:

        """
        Get the axis value

        :return: List[float], the axis value
        """

        return self['axis'].value

    @property
    def axisX(self) -> float:

        """
        Get the axisX value

        :return: float, the axisX value
        """

        return self['axisX'].asFloat()

    @property
    def axisY(self) -> float:

        """
        Get the axisY value

        :return: float, the axisY value
        """

        return self['axisY'].asFloat()

    @property
    def axisZ(self) -> float:

        """
        Get the axisZ value

        :return: float, the axisZ value
        """

        return self['axisZ'].asFloat()


NodeRegistry()[AngleBetween.nodeType()] = AngleBetween
