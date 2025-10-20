from typing import Optional, Union, List

from maya import cmds as mc
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


class IkSolver(DGNode):

    _NODE_TYPE = "ikSolver"
    _API_TYPE = om.MFn.kIkSolver

    @property
    def solverType(self):
        return NotImplementedError(
            f'{self.__class__.__name__}.solverType is not implemented'
        )


NodeRegistry()[IkHandle.nodeType()] = IkHandle
NodeRegistry()[IkSolver.nodeType()] = IkSolver
