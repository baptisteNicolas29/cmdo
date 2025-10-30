from typing import Optional, List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class HoldMatrix(dgLib.DGNode):

    _NODE_TYPE = "holdMatrix"
    _API_TYPE = om.MFn.kMatrixHold

    @property
    def inMatrix(self) -> Union[List[float], om.MMatrix]:
        """
        Get the inMatrix value

        :return: Union[List[float], om.MMatrix], the inMatrix value
        """

        return self['inMatrix'].value

    @inMatrix.setter
    def inMatrix(self, value: Union[List[float], om.MMatrix, om.MPlug]) -> None:

        """
        Set the inMatrix value

        Args:
            value: Union[List[float], om.MMatrix, om.MPlug], the inMatrix value
        """

        self['inMatrix'] = value

    @property
    def outMatrix(self) -> Union[List[float], om.MMatrix]:
        """
        Get the outMatrix value

        :return: Union[List[float], om.MMatrix], the outMatrix value
        """

        return self['outMatrix'].value


NodeRegistry()[HoldMatrix.nodeType()] = HoldMatrix
