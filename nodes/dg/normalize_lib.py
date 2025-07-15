from typing import List

from maya.api import OpenMaya as om

from ...core.abstract import dg_lib
from ...core.node_registry import NodeRegistry


class Normalize(dg_lib.DGNode):

    _NODE_TYPE = "normalize"
    _API_TYPE = om.MFn.kNormalize

    def __init__(self, name: str | om.MObject = None) -> None:
        """
        Initialize an instance of Normalize

        Args:
            name: str | om.MObject, the name of the node
        """

        super().__init__(name=name)

    @property
    def input(self) -> List[float]:
        """
        Get the input value

        Returns:
            List[float]: the input value
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

        Args:
            value: List[float], the input value
        """

        self['input'] = value

    @property
    def inputX(self) -> float:
        """
        Get the inputX value

        Returns:
            List[float]: the inputX value
        """

        return self['inputX'].asFloat()

    @inputX.setter
    def inputX(self, value: float) -> None:
        """
        Set the inputX value

        Args:
            value: List[float], the inputX value
        """

        self['inputX'] = value

    @property
    def inputY(self) -> float:
        """
        Get the inputY value

        Returns:
            List[float]: the inputY value
        """

        return self['inputY'].asFloat()

    @inputY.setter
    def inputY(self, value: float) -> None:
        """
        Set the inputY value

        Args:
            value: List[float], the inputY value
        """

        self['inputY'] = value

    @property
    def inputZ(self) -> float:
        """
        Get the inputZ value

        Returns:
            List[float]: the inputZ value
        """

        return self['inputZ'].asFloat()

    @inputZ.setter
    def inputZ(self, value: float) -> None:
        """
        Set the inputZ value

        Args:
            value: List[float], the inputZ value
        """

        self['inputZ'] = value


    @property
    def output(self) -> List[float]:
        """
        Get the output value

        Returns:
            List[float]: the output value
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

        Returns:
            List[float]: the outputX value
        """

        return self['outputX'].asFloat()


    @property
    def outputY(self) -> float:
        """
        Get the outputY value

        Returns:
            List[float]: the outputY value
        """

        return self['outputY'].asFloat()


    @property
    def outputZ(self) -> float:
        """
        Get the outputZ value

        Returns:
            List[float]: the outputZ value
        """

        return self['outputZ'].asFloat()


NodeRegistry()[Normalize.nodeType()] = Normalize
