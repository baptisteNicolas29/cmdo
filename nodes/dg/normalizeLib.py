from typing import List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class Normalize(dgLib.DGNode):

    _NODE_TYPE = "normalize"
    _API_TYPE = om.MFn.kNormalize

    @property
    def input(self) -> List[float]:
        """
        Get the input value

        :return: List[float], the input value
        """

        return [
            self.inputX,
            self.inputY,
            self.inputZ
        ]

    @input.setter
    def input(self, value: List[float]) -> None:
        """
        Set the input value

        :param value: List[float], the input value
        """

        self['input'] = value

    @property
    def inputX(self) -> float:
        """
        Get the inputX value

        :return: List[float], the inputX value
        """

        return self['inputX'].asFloat()

    @inputX.setter
    def inputX(self, value: float) -> None:
        """
        Set the inputX value

        :param value: List[float], the inputX value
        """

        self['inputX'] = value

    @property
    def inputY(self) -> float:
        """
        Get the inputY value

        :return: List[float], the inputY value
        """

        return self['inputY'].asFloat()

    @inputY.setter
    def inputY(self, value: float) -> None:
        """
        Set the inputY value

        :param value: List[float], the inputY value
        """

        self['inputY'] = value

    @property
    def inputZ(self) -> float:
        """
        Get the inputZ value

        :return: List[float], the inputZ value
        """

        return self['inputZ'].asFloat()

    @inputZ.setter
    def inputZ(self, value: float) -> None:
        """
        Set the inputZ value

        :param value: List[float], the inputZ value
        """

        self['inputZ'] = value

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

    @property
    def outputX(self) -> float:
        """
        Get the outputX value

        :return: List[float], the outputX value
        """

        return self['outputX'].asFloat()

    @property
    def outputY(self) -> float:
        """
        Get the outputY value

        :return: List[float], the outputY value
        """

        return self['outputY'].asFloat()

    @property
    def outputZ(self) -> float:
        """
        Get the outputZ value

        :return: List[float], the outputZ value
        """

        return self['outputZ'].asFloat()


NodeRegistry()[Normalize.nodeType()] = Normalize
