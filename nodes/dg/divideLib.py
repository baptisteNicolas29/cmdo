from typing import Optional, List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class Divide(dgLib.DGNode):

    _NODE_TYPE = "divide"
    _API_TYPE = om.MFn.kDivide

    @property
    def input1(self) -> float:
        """
        Get the input1 value

        :return: List[float] the input1 value
        """

        return self['input1'].asFloat()

    @input1.setter
    def input1(self, value: float):
        """
        Set the input1 value

        :param value: float, the input1 value
        """

        self['input1'] = value

    @property
    def input2(self) -> float:
        """
        Get the input2 value

        :return: float the input2 value
        """

        return self['input2'].asFloat()

    @input2.setter
    def input2(self, value: float):
        """
        Set the input2 value

        :param value: List[float], the input2 value
        """

        self['input2'] = value

    @property
    def output(self) -> float:
        """
        Get the output value

        :return: float the output value
        """

        return self['output'].asFloat()


NodeRegistry()[Divide.nodeType()] = Divide
