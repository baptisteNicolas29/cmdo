from typing import List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dg_lib
from ...core.node_registry import NodeRegistry


class PointMatrixMult(dg_lib.DGNode):

    _NODE_TYPE = "pointMatrixMult"
    _API_TYPE = om.MFn.kPointMatrixMult

    def __init__(self, name: Union[str, om.MObject] = None) -> None:
        """
        Initialize an instance of PointMatrixMult

        Args:
            name: str | om.MObject, the name of the node
        """

        super().__init__(name=name)

    @property
    def inMatrix(self) -> List[float]:
        """
        Get the inMatrix value

        Returns:
            List[float]: the inMatrix value
        """

        return self['inMatrix'].value

    @inMatrix.setter
    def inMatrix(self, value: List[float]) -> None:
        """
        Set the inMatrix value

        Args:
            value: List[float] the inMatrix value
        """

        self['inMatrix'] = value

    @property
    def inPoint(self) -> List[float]:
        """
        Get the inPoint value

        Returns:
            List[float]: the inPoint value
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

        Args:
            value: List[float], the inPoint value
        """

        self['inPoint'] = value

    @property
    def inPointX(self) -> float:
        """
        Get the inPointX value

        Returns:
            float: the inPointX value
        """

        return self['inPointX'].asFloat()

    @inPointX.setter
    def inPointX(self, value: float) -> None:
        """
        Set the inPointX value

        Args:
            value: float, the inPointX value
        """

        self['inPointX'] = value

    @property
    def inPointY(self) -> float:
        """
        Get the inPointY value

        Returns:
            float: the inPointY value
        """

        return self['inPointY'].asFloat()

    @inPointY.setter
    def inPointY(self, value: float) -> None:
        """
        Set the inPointY value

        Args:
            value: float, the inPointY value
        """

        self['inPointY'] = value

    @property
    def inPointZ(self) -> float:
        """
        Get the inPointZ value

        Returns:
            float: the inPointZ value
        """

        return self['inPointZ'].asFloat()

    @inPointZ.setter
    def inPointZ(self, value: float) -> None:
        """
        Set the inPointZ value

        Args:
            value: float, the inPointZ value
        """

        self['inPointZ'] = value

    @property
    def vectorMultiply(self) -> bool:
        """
        Get the vectorMultiply value

        Returns:
            bool: the vectorMultiply value
        """

        return self['vectorMultiply'].asBool()

    @vectorMultiply.setter
    def vectorMultiply(self, value: bool) -> None:
        """
        Set the vectorMultiply value

        Args:
            value: bool, the vectorMultiply value
        """

        self['vectorMultiply'] = value

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

    @output.setter
    def output(self, value: List[float]):
        """
        Set the output value

        Args:
            value: List[float], the output value
        """

        self['output'] = value

    @property
    def outputX(self) -> float:
        """
        Get the outputX value

        Returns:
            float: the outputX value
        """

        return self['outputX'].asFloat()

    @outputX.setter
    def outputX(self, value: float) -> None:
        """
        Set the outputX value

        Args:
            value: float, the outputX value
        """

        self['outputX'] = value

    @property
    def outputY(self) -> float:
        """
        Get the outputY value

        Returns:
            float: the outputY value
        """

        return self['outputY'].asFloat()

    @outputY.setter
    def outputY(self, value: float) -> None:
        """
        Set the outputY value

        Args:
            value: float, the outputY value
        """

        self['outputY'] = value

    @property
    def outputZ(self) -> float:
        """
        Get the outputZ value

        Returns:
            float: the outputZ value
        """

        return self['outputZ'].asFloat()

    @outputZ.setter
    def outputZ(self, value: float) -> None:
        """
        Set the outputZ value

        Args:
            value: float, the outputZ value
        """

        self['outputZ'] = value


NodeRegistry()[PointMatrixMult.nodeType()] = PointMatrixMult
