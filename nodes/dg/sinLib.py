from typing import List

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class Sin(dgLib.DGNode):

    _NODE_TYPE = "sin"
    _API_TYPE = om.MFn.kSin

    @property
    def input(self) -> List[float]:
        """
        Get the input value

        :return: List[float] the input value
        """

        return self['input'].asFloat()

    @input.setter
    def input(self, value: List[float]):
        """
        Set the input value

        :param value: List[float], the input value
        """

        self['input'] = value

    @property
    def output(self) -> List[float]:
        """
        Get the output value

        :return: List[float] the output value
        """

        return self['output'].asFloat()

    @output.setter
    def output(self, value: List[float]):
        """
        Set the output value

        :param value: List[float], the output value
        """

        self['output'] = value


NodeRegistry()[Sin.nodeType()] = Sin
