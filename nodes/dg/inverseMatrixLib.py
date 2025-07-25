from typing import Optional, Union, List

from maya.api import OpenMaya as om

from ...core import convert
from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class InverseMatrix(dgLib.DGNode):

    _NODE_TYPE = "inverseMatrix"
    _API_TYPE = om.MFn.kPluginDependNode

    def __init__(self, name: Union[str, om.MObject] = None) -> None:
        """
        Initialize an instance of InverseMatrix

        Args:
            name: str | om.MObject, the name of the node
        """

        super().__init__(name=name)

    @property
    def inputMatrix(self) -> List[float]:
        """
        Get the inputMatrix value

        Returns:
            List[float]: the inputMatrix value
        """

        return self['inputMatrix'].value

    @inputMatrix.setter
    def inputMatrix(self, value: List[float]) -> None:
        """
        Set the inputMatrix value

        Args:
            value: List[float] the inputMatrix value
        """

        self['inputMatrix'] = value

    @property
    def outputMatrix(self) -> List[float]:
        """
        Get the outputMatrix value

        Returns:
            List[float]: the outputMatrix value
        """

        return self['outputMatrix'].value


NodeRegistry()[InverseMatrix.nodeType()] = InverseMatrix
