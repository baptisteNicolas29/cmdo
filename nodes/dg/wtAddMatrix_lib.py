from typing import List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dg_lib
from ...core.node_registry import NodeRegistry


class WtAddMatrix(dg_lib.DGNode):

    _NODE_TYPE = "wtAddMatrix"
    _API_TYPE = om.MFn.kMatrixWtAdd

    def __init__(self, name: Union[str, om.MObject] = None) -> None:

        """
        Initialize an instance of WtAddMatrix

        Args:
            name: str | om.MObject, the name of the node
        """

        super().__init__(name=name)

    @property
    def wtMatrixCount(self) -> int:
        """
        Get the number of child wtMatrix attributes
        from the compound (numElements)

        Returns:
            int: the number of child wtMatrix attributes from the compound
        """

        return self['wtMatrix'].numElements()

    @property
    def wtMatrix(self) -> om.MPlug:
        """
        Get the wtMatrix parent plug

        Returns:
            om.MPlug: the wtMatrix parent plug
        """

        return self['wtMatrix']

    @property
    def matrixSum(self) -> List[float]:
        """
        Get the matrixSum value

        Returns:
             List[float]: the matrixSum value
        """

        return self['matrixSum'].value

    def getWtMatrix(self, index: int) -> om.MPlug:
        """
        Get the wtMatrix from a target index value

        Args:
            index: int, the index of the wtMatrix to get

        Returns:
            om.MPlug: the wtMatrix value
        """

        return self['wtMatrix'][index]

    def setWtMatrix(self, index: int, value: om.MPlug) -> None:
        """
        Set the wtMatrix from a target index value

        Args:
            index: int, the index of the wtMatrix to get
            value: om.MPlug, the plug to connect to wtMatrix
        """

        self['wtMatrix'][index] = value

    def getMatrixIn(self, index: int) -> List[float]:
        """
        Get the matrixIn from a target index value

        Args:
            index: int, the index of the matrixIn to get

        Returns:
            List[float]: the matrixIn value
        """

        return self['wtMatrix'][index]['matrixIn'].value

    def setMatrixIn(self, index: int, value: Union[List[float], om.MPlug]) -> None:
        """
        Set the matrixIn from a target index value

        Args:
            index: int, the index of the matrixIn to get
            value: List[float] | om.MPlug, the matrixIn value
        """

        self['wtMatrix'][index]['matrixIn'] = value

    def getWeightIn(self, index: int) -> float:
        """
        Get the weightIn from a target index value

        Args:
            index: int, the index of the weightIn to get

        Returns:
            float: the weightIn value
        """

        return self['wtMatrix'][index]['weightIn'].value

    def setWeightIn(self, index: int, value: Union[float, om.MPlug]) -> None:
        """
        Set the weightIn from a target index value

        Args:
            index: int, the index of the weightIn to get
            value: float | om.MPlug, the weightIn value
        """

        self['wtMatrix'][index]['weightIn'] = value


NodeRegistry()[WtAddMatrix.nodeType()] = WtAddMatrix
