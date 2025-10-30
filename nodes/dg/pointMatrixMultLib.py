from typing import List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class PointMatrixMult(dgLib.DGNode):

    _NODE_TYPE = "pointMatrixMult"
    _API_TYPE = om.MFn.kPointMatrixMult

    @property
    def inMatrix(self) -> List[float]:
        """
        Get the inMatrix value

        :return: List[float], the inMatrix value
        """

        return self['inMatrix'].value

    @inMatrix.setter
    def inMatrix(self, value: List[float]) -> None:
        """
        Set the inMatrix value

        :param value: List[float] the inMatrix value
        """

        self['inMatrix'] = value

    @property
    def inPoint(self) -> List[float]:
        """
        Get the inPoint value

        :return: List[float], the inPoint value
        """

        return [
            self.inPointX,
            self.inPointY,
            self.inPointZ
        ]

    @inPoint.setter
    def inPoint(self, value: List[float]):
        """
        Set the inPoint value

        :param value: List[float], the inPoint value
        """

        self['inPoint'] = value

    @property
    def inPointX(self) -> float:
        """
        Get the inPointX value

        :return: float, the inPointX value
        """

        return self['inPointX'].asFloat()

    @inPointX.setter
    def inPointX(self, value: float) -> None:
        """
        Set the inPointX value

        :param value: float, the inPointX value
        """

        self['inPointX'] = value

    @property
    def inPointY(self) -> float:
        """
        Get the inPointY value

        :return: float, the inPointY value
        """

        return self['inPointY'].asFloat()

    @inPointY.setter
    def inPointY(self, value: float) -> None:
        """
        Set the inPointY value

        :param value: float, the inPointY value
        """

        self['inPointY'] = value

    @property
    def inPointZ(self) -> float:
        """
        Get the inPointZ value

        :return: float, the inPointZ value
        """

        return self['inPointZ'].asFloat()

    @inPointZ.setter
    def inPointZ(self, value: float) -> None:
        """
        Set the inPointZ value

        :param value: float, the inPointZ value
        """

        self['inPointZ'] = value

    @property
    def vectorMultiply(self) -> bool:
        """
        Get the vectorMultiply value

        :return: bool, the vectorMultiply value
        """

        return self['vectorMultiply'].asBool()

    @vectorMultiply.setter
    def vectorMultiply(self, value: bool) -> None:
        """
        Set the vectorMultiply value

        :param value: bool, the vectorMultiply value
        """

        self['vectorMultiply'] = value

    @property
    def output(self) -> List[float]:
        """
        Get the output value

        :return: List[float], the output value
        """

        return [
            self.outputX,
            self.outputY,
            self.outputZ
        ]

    @output.setter
    def output(self, value: List[float]):
        """
        Set the output value

        :param value: List[float], the output value
        """

        self['output'] = value

    @property
    def outputX(self) -> float:
        """
        Get the outputX value

        :return: float, the outputX value
        """

        return self['outputX'].asFloat()

    @outputX.setter
    def outputX(self, value: float) -> None:
        """
        Set the outputX value

        :param value: float, the outputX value
        """

        self['outputX'] = value

    @property
    def outputY(self) -> float:
        """
        Get the outputY value

        :return: float, the outputY value
        """

        return self['outputY'].asFloat()

    @outputY.setter
    def outputY(self, value: float) -> None:
        """
        Set the outputY value

        :param value: float, the outputY value
        """

        self['outputY'] = value

    @property
    def outputZ(self) -> float:
        """
        Get the outputZ value

        :return: float, the outputZ value
        """

        return self['outputZ'].asFloat()

    @outputZ.setter
    def outputZ(self, value: float) -> None:
        """
        Set the outputZ value

        :param value: float, the outputZ value
        """

        self['outputZ'] = value


NodeRegistry()[PointMatrixMult.nodeType()] = PointMatrixMult
