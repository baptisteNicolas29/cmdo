from typing import Optional, Union, List

from maya import cmds, mel
from maya.api import OpenMaya as om, OpenMayaAnim as oma

from ...core.nodeRegistry import NodeRegistry
from ...core.abstract.dgLib import DGNode
from ...core.plugsLib import Plug
from .transformLib import Transform


class IkHandle(Transform):

    _NODE_TYPE = "ikHandle"
    _API_TYPE = om.MFn.kIkHandle

    @property
    def dForwardAxisList(self) -> List[str]:

        return [
            'positiveX', 'negativeX',
            'positiveY', 'negativeY',
            'positiveZ', 'negativeZ'
        ]

    @property
    def dWorldUpAxisList(self) -> List[str]:

        return [
            'positiveY', 'negativeY', 'closestY',
            'positiveZ', 'negativeZ', 'closestZ',
            'positiveX', 'negativeX', 'closestX',
        ]

    @property
    def ikSolver(self):

        return IkSolver(self['ikSolver'].source().node())

    @property
    def endEffector(self):
        return IkSolver(self['ikSolver'].source().node())

    @property
    def dTwistControlEnable(self) -> bool:

        return self['dTwistControlEnable'].asBool()

    @dTwistControlEnable.setter
    def dTwistControlEnable(self, value: bool) -> None:

        self['dTwistControlEnable'] = value

    @property
    def dForwardAxis(self) -> int:

        return self['dForwardAxis'].asInt()

    @dForwardAxis.setter
    def dForwardAxis(self, value: Union[int, str]) -> None:
        if isinstance(value, int):
            self['dForwardAxis'] = value

        elif isinstance(value, str) and value in self.dForwardAxisList:
            self['dForwardAxis'] = self.dForwardAxisList.index(value)

    @property
    def dWorldUpAxis(self) -> int:

        return self['dWorldUpAxis'].asInt()

    @dWorldUpAxis.setter
    def dWorldUpAxis(self, value: Union[int, str]) -> None:
        if isinstance(value, int):
            self['dWorldUpAxis'] = value

        elif isinstance(value, str) and value in self.dWorldUpAxisList:
            self['dWorldUpAxis'] = self.dWorldUpAxisList.index(value)

    @property
    def dWorldUpType(self) -> int:

        return self['dWorldUpType'].asInt()

    @dWorldUpType.setter
    def dWorldUpType(self, value: int) -> None:

        self['dWorldUpType'] = value

    @property
    def dWorldUpMatrix(self) -> om.MMatrix:

        return self['dWorldUpMatrix'].value

    @dWorldUpMatrix.setter
    def dWorldUpMatrix(self, value: Plug) -> None:

        self['dWorldUpMatrix'] = value

    @property
    def dWorldUpMatrixEnd(self) -> om.MMatrix:
        return self['dWorldUpMatrixEnd'].value

    @dWorldUpMatrixEnd.setter
    def dWorldUpMatrixEnd(self, value: Plug) -> None:
        self['dWorldUpMatrixEnd'] = value

    @property
    def dWorldUpVector(self) -> List[float]:

        """
        Get the dWorldUpVector value

        Returns:
            List[float]: the dWorldUpVector value
        """

        return [
            self.dWorldUpVectorX,
            self.dWorldUpVectorY,
            self.dWorldUpVectorZ
        ]

    @dWorldUpVector.setter
    def dWorldUpVector(self, value):

        """
        Set the dWorldUpVector value

        Args:
            value: List[float], the dWorldUpVector value
        """

        self['dWorldUpVector'] = value

    @property
    def dWorldUpVectorX(self) -> float:

        """
        Get the dWorldUpVectorX value

        Returns:
            List[float]: the dWorldUpVectorX value
        """

        return self['dWorldUpVectorX'].asFloat()

    @dWorldUpVectorX.setter
    def dWorldUpVectorX(self, value) -> None:

        """
        Set the dWorldUpVectorX value

        Args:
            value: List[float], the dWorldUpVectorX value
        """

        self['dWorldUpVectorX'] = value

    @property
    def dWorldUpVectorY(self) -> float:

        """
        Get the dWorldUpVectorY value

        Returns:
            List[float]: the dWorldUpVectorY value
        """

        return self['dWorldUpVectorY'].asFloat()

    @dWorldUpVectorY.setter
    def dWorldUpVectorY(self, value) -> None:

        """
        Set the dWorldUpVectorY value

        Args:
            value: List[float], the dWorldUpVectorY value
        """

        self['dWorldUpVectorY'] = value

    @property
    def dWorldUpVectorZ(self) -> float:

        """
        Get the dWorldUpVectorZ value

        Returns:
            List[float]: the dWorldUpVector value
        """

        return self['dWorldUpVectorZ'].asFloat()

    @dWorldUpVectorZ.setter
    def dWorldUpVectorZ(self, value) -> None:

        """
        Set the dWorldUpVectorZ value

        Args:
            value: List[float], the dWorldUpVectorZ value
        """

        self['dWorldUpVectorZ'] = value

    @property
    def dWorldUpVectorEnd(self) -> List[float]:

        """
        Get the dWorldUpVectorEnd value

        Returns:
            List[float]: the dWorldUpVectorEnd value
        """

        return [
            self.dWorldUpVectorEndX,
            self.dWorldUpVectorEndY,
            self.dWorldUpVectorEndZ
        ]

    @dWorldUpVectorEnd.setter
    def dWorldUpVectorEnd(self, value):

        """
        Set the dWorldUpVectorEnd value

        Args:
            value: List[float], the dWorldUpVectorEnd value
        """

        self['dWorldUpVectorEnd'] = value

    @property
    def dWorldUpVectorEndX(self) -> float:

        """
        Get the dWorldUpVectorEndX value

        Returns:
            List[float]: the dWorldUpVectorEndX value
        """

        return self['dWorldUpVectorEndX'].asFloat()

    @dWorldUpVectorEndX.setter
    def dWorldUpVectorEndX(self, value) -> None:

        """
        Set the dWorldUpVectorEndX value

        Args:
            value: List[float], the dWorldUpVectorEndX value
        """

        self['dWorldUpVectorEndX'] = value

    @property
    def dWorldUpVectorEndY(self) -> float:

        """
        Get the dWorldUpVectorEndY value

        Returns:
            List[float]: the dWorldUpVectorEndY value
        """

        return self['dWorldUpVectorEndY'].asFloat()

    @dWorldUpVectorEndY.setter
    def dWorldUpVectorEndY(self, value) -> None:

        """
        Set the dWorldUpVectorEndY value

        Args:
            value: List[float], the dWorldUpVectorEndY value
        """

        self['dWorldUpVectorEndY'] = value

    @property
    def dWorldUpVectorEndZ(self) -> float:

        """
        Get the dWorldUpVectorEndZ value

        Returns:
            List[float]: the dWorldUpVectorEnd value
        """

        return self['dWorldUpVectorEndZ'].asFloat()

    @dWorldUpVectorEndZ.setter
    def dWorldUpVectorEndZ(self, value) -> None:

        """
        Set the dWorldUpVectorEndZ value

        Args:
            value: List[float], the dWorldUpVectorEndZ value
        """

        self['dWorldUpVectorEndZ'] = value
    

class IkSolver(DGNode):

    _NODE_TYPE = "ikSolver"
    _API_TYPE = om.MFn.kIkSolver

    @property
    def solverType(self):
        return cmds.nodeType(self.name)


class IkSCSolver(IkSolver):

    _NODE_TYPE = "ikSCsolver"
    _API_TYPE = om.MFn.kIkSolver


class IkRPSolver(IkSolver):

    _NODE_TYPE = "ikRPsolver"
    _API_TYPE = om.MFn.kIkSolver


class IkSplineSolver(IkSolver):

    _NODE_TYPE = "ikSplineSolver"
    _API_TYPE = om.MFn.kIkSolver


class IkSpringSolver(IkSolver):

    _NODE_TYPE = "ikSpringSolver"
    _API_TYPE = om.MFn.kIkSolver

    def __init__(self, name: Union[str, om.MObject] = None):
        super().__init__(name)

        mel.eval('ikSpringSolver')


NodeRegistry()[IkHandle.nodeType()] = IkHandle
NodeRegistry()[IkSolver.nodeType()] = IkSolver
NodeRegistry()[IkSCSolver.nodeType()] = IkSCSolver
NodeRegistry()[IkRPSolver.nodeType()] = IkRPSolver
NodeRegistry()[IkSplineSolver.nodeType()] = IkSplineSolver
NodeRegistry()[IkSpringSolver.nodeType()] = IkSpringSolver
