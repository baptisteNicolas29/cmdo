from typing import Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class ClampRange(dgLib.DGNode):

    _NODE_TYPE = "clampRange"
    _API_TYPE = om.MFn.kClampRange

    @property
    def input(self) -> float:

        """
        Get the input value

        :return: float, the input value
        """

        return self['input'].asFloat()

    @input.setter
    def input(self, value: float) -> None:

        """
        Set the input value

        :param value: float, the input value
        """

        self['input'] = value

    @property
    def minimum(self) -> float:
        """
        Get the minimum value

        :return: float, the minimum value
        """

        return self['minimum'].asFloat()

    @minimum.setter
    def minimum(self, value: float) -> None:
        """
        Set the minimum value

        :param value: float, the minimum value
        """

        self['minimum'] = value

    @property
    def maximum(self) -> float:
        """
        Get the maximum value

        :return: float, the maximum value
        """

        return self['maximum'].asFloat()

    @maximum.setter
    def maximum(self, value: float) -> None:
        """
        Set the maximum value

        :param value: float, the maximum value
        """

        self['maximum'] = value

    @property
    def output(self) -> float:
        """
        Get the output value

        :return: float, the output value
        """

        return self['output'].asFloat()
        

NodeRegistry()[ClampRange.nodeType()] = ClampRange
