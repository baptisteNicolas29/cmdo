from typing import List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class DistanceBetween(dgLib.DGNode):

    _NODE_TYPE = "distanceBetween"
    _API_TYPE = om.MFn.kDistanceBetween

    @property
    def point1(self) -> List[float]:
        """
        Get the point1 value

        :return: List[float], the point1 value
        """

        return [
            self.point1X,
            self.point1Y,
            self.point1Z
        ]

    @point1.setter
    def point1(self, value: List[float]) -> None:
        """
        Set the point1 value

        :param value: List[float], the point1 value
        """

        self['point1'] = value

    @property
    def point1X(self) -> float:
        """
        Get the point1X value

        :return: List[float], the point1X value
        """

        return self['point1X'].asFloat()

    @point1X.setter
    def point1X(self, value: float) -> None:
        """
        Set the point1X value

        :param value: List[float], the point1X value
        """

        self['point1X'] = value

    @property
    def point1Y(self) -> float:
        """
        Get the point1Y value

        :return: List[float], the point1Y value
        """

        return self['point1Y'].asFloat()

    @point1Y.setter
    def point1Y(self, value: float) -> None:
        """
        Set the point1Y value

        :param value: List[float], the point1Y value
        """

        self['point1Y'] = value

    @property
    def point1Z(self) -> float:
        """
        Get the point1Z value

        :return: List[float], the point1Z value
        """

        return self['point1Z'].asFloat()

    @point1Z.setter
    def point1Z(self, value: float) -> None:
        """
        Set the point1Z value

        :param value: List[float], the point1Z value
        """

        self['point1Z'] = value

    @property
    def point2(self) -> List[float]:
        """
        Get the point2 value

        :return: List[float], the point2 value
        """

        return [
            self.point2X,
            self.point2Y,
            self.point2Z
        ]

    @point2.setter
    def point2(self, value: List[float]):
        """
        Set the point2 value

        :param value: List[float], the point2 value
        """

        self['point2'] = value

    @property
    def point2X(self) -> float:
        """
        Get the point2X value

        :return: List[float], the point2X value
        """

        return self['point2X'].asFloat()

    @point2X.setter
    def point2X(self, value: float) -> None:
        """
        Set the point2X value

        :param value: List[float], the point2X value
        """

        self['point2X'] = value

    @property
    def point2Y(self) -> float:
        """
        Get the point2Y value

        :return: List[float], the point2Y value
        """

        return self['point2Y'].asFloat()

    @point2Y.setter
    def point2Y(self, value: float) -> None:
        """
        Set the point2Y value

        :param value: List[float], the point2Y value
        """

        self['point2Y'] = value

    @property
    def point2Z(self) -> float:
        """
        Get the point2Z value

        :return: List[float], the point2Z value
        """

        return self['point2Z'].asFloat()

    @point2Z.setter
    def point2Z(self, value: float) -> None:
        """
        Set the point2Z value

        :param value: List[float], the point2Z value
        """

        self['point2Z'] = value

    @property
    def inMatrix1(self) -> List[float]:
        """
        Get the inMatrix1 value

        :return: List[float], the inMatrix1 value
        """

        return self['inMatrix1'].value

    @inMatrix1.setter
    def inMatrix1(self, value: List[float]):
        """
        Set the inMatrix1 value

        :param value: List[float], the inMatrix1 value
        """

        self['inMatrix1'] = value

    @property
    def inMatrix2(self) -> List[float]:
        """
        Get the inMatrix2 value

        :return: List[float], the inMatrix2 value
        """

        return self['inMatrix2'].value

    @inMatrix2.setter
    def inMatrix2(self, value: List[float]):
        """
        Set the inMatrix2 value

        :param value: List[float], the inMatrix2 value
        """

        self['inMatrix2'] = value

    @property
    def distance(self) -> float:
        """
        Get the distance value

        :return: List[float], the distance value
        """

        return self['distance'].value


NodeRegistry()[DistanceBetween.nodeType()] = DistanceBetween
