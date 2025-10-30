from typing import Optional, List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class PickMatrix(dgLib.DGNode):

    _NODE_TYPE = "pickMatrix"
    _API_TYPE = om.MFn.kPickMatrix

    @property
    def inputMatrix(self) -> List[float]:

        """
        Get the inputMatrix value

        :return: List[float], the inputMatrix value
        """

        return self['inputMatrix'].value

    @inputMatrix.setter
    def inputMatrix(self, value: List[float]) -> None:
        """
        Set the inputMatrix value

        :param value: List[float], the inputMatrix value
        """

        self['inputMatrix'] = value

    @property
    def useTranslate(self) -> bool:
        """
        Get the useTranslate value

        :return: bool, the useTranslate value
        """

        return self['useTranslate'].asBool()

    @useTranslate.setter
    def useTranslate(self, value: bool) -> None:
        """
        Set the useTranslate value

        :param value: bool, the useTranslate value
        """

        self['useTranslate'] = value

    @property
    def useRotate(self) -> bool:
        """
        Get the useRotate value

        :return: bool, the useRotate value
        """

        return self['useRotate'].asBool()

    @useRotate.setter
    def useRotate(self, value: bool) -> None:
        """
        Set the useRotate value

        :param value: bool, the useRotate value
        """

        self['useRotate'] = value

    @property
    def useScale(self) -> bool:
        """
        Get the useScale value

        :return: bool, the useScale value
        """

        return self['useScale'].asBool()

    @useScale.setter
    def useScale(self, value: bool) -> None:
        """
        Set the useScale value

        :param value: bool, the useScale value
        """

        self['useScale'] = value

    @property
    def useShear(self) -> bool:
        """
        Get the useShear value

        :return: bool, the useShear value
        """

        return self['useShear'].asBool()

    @useShear.setter
    def useShear(self, value: bool) -> None:
        """
        Set the useShear value

        :param value: bool, the useShear value
        """

        self['useShear'] = value

    @property
    def outputMatrix(self) -> List[float]:
        """
        Get the outputMatrix value

        :return: bool, the outputMatrix value
        """

        return self['outputMatrix'].value


NodeRegistry()[PickMatrix.nodeType()] = PickMatrix
