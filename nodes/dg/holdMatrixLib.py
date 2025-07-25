from typing import Optional, List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class HoldMatrix(dgLib.DGNode):

    _NODE_TYPE = "holdMatrix"
    _API_TYPE = om.MFn.kMatrixHold

    def __init__(self, name: Union[str, om.MObject] = None) -> None:
        """
        Initialize an instance of HoldMatrix

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
    def outMatrix(self) -> List[float]:
        """
        Get the outMatrix value

        Returns:
            List[float]: the outMatrix value
        """

        return self['outMatrix'].value


NodeRegistry()[HoldMatrix.nodeType()] = HoldMatrix
