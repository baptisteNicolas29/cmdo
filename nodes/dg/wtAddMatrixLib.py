from typing import List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class WtAddMatrix(dgLib.DGNode):

    _NODE_TYPE = "wtAddMatrix"
    _API_TYPE = om.MFn.kMatrixWtAdd

    @property
    def wtMatrixCount(self) -> int:
        """
        Get the number of child wtMatrix attributes
        from the compound (numElements)

        :return: int, the number of child wtMatrix attributes from the compound
        """

        return self['wtMatrix'].numElements()

    @property
    def wtMatrix(self) -> om.MPlug:
        """
        Get the wtMatrix parent plug

        :return: om.MPlug, the wtMatrix parent plug
        """

        return self['wtMatrix']

    @property
    def matrixSum(self) -> List[float]:
        """
        Get the matrixSum value

        :return: List[float], the matrixSum value
        """

        return self['matrixSum'].value

    def getWtMatrix(self, index: int) -> om.MPlug:
        """
        Get the wtMatrix from a target index value

        :param index: int, the index of the wtMatrix to get

        :return: om.MPlug, the wtMatrix value
        """

        return self['wtMatrix'][index]

    def setWtMatrix(self, index: int, value: om.MPlug) -> None:
        """
        Set the wtMatrix from a target index value

        :param index: int, the index of the wtMatrix to get
        :param value: om.MPlug, the plug to connect to wtMatrix
        """

        self['wtMatrix'][index] = value

    def getMatrixIn(self, index: int) -> List[float]:
        """
        Get the matrixIn from a target index value

        :param index: int, the index of the matrixIn to get

        :return: List[float], the matrixIn value
        """

        return self['wtMatrix'][index]['matrixIn'].value

    def setMatrixIn(self, index: int, value: Union[List[float], om.MPlug]) -> None:
        """
        Set the matrixIn from a target index value

        :param index: int, the index of the matrixIn to get
        :param value: Union[List[float], om.MPlug], the matrixIn value
        """

        self['wtMatrix'][index]['matrixIn'] = value

    def getWeightIn(self, index: int) -> float:
        """
        Get the weightIn from a target index value

        :param index: int, the index of the weightIn to get

        :return: float, the weightIn value
        """

        return self['wtMatrix'][index]['weightIn'].value

    def setWeightIn(self, index: int, value: Union[float, om.MPlug]) -> None:
        """
        Set the weightIn from a target index value

        :param index: int, the index of the weightIn to get
        :param value: Union[float, om.MPlug], the weightIn value
        """

        self['wtMatrix'][index]['weightIn'] = value


NodeRegistry()[WtAddMatrix.nodeType()] = WtAddMatrix
