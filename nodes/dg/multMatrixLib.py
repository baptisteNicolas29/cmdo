from typing import List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class MultMatrix(dgLib.DGNode):

    _NODE_TYPE = "multMatrix"
    _API_TYPE = om.MFn.kMatrixMult

    def __init__(self, name: Union[str, om.MObject] = None) -> None:
        """
        Initialize an instance of MultMatrix

        Args:
            name: str | om.MObject, the name of the node
        """

        super().__init__(name=name)

    @property
    def matrixInCount(self) -> int:
        """
        Get the number of matrixIn compound attributes (numElements)

        Returns:
            int: the number of matrixIn compound attributes
        """

        return self['matrixIn'].numElements()

    def getMatrixIn(self, index: int) -> List[float]:
        """
        Get the matrixIn from a target index value

        Args:
            index: int, the index of the matrix to get

        Returns:
            List[float]: the matrixIn value
        """

        return self['matrixIn'][index].value

    def setMatrixIn(self, index: int, value: Union[List[float], om.MPlug]) -> None:
        """
        Set the matrixIn from a target index value

        Args:
            index: int, the index of the matrix to get
            value: List[float], the matrixIn value
        """

        self['matrixIn'][index] = value

    @property
    def matrixSum(self) -> List[float]:
        """
        Get the matrixSum value

        Returns:
            int: the matrixSum value
        """

        return self['matrixSum'].value


NodeRegistry()[MultMatrix.nodeType()] = MultMatrix
