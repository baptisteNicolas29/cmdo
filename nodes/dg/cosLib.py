from typing import Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class Cos(dgLib.DGNode):

    _NODE_TYPE = "cos"
    _API_TYPE = om.MFn.kCos

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
    def output(self) -> float:
        """
        Get the output value

        :return: float, the output value
        """

        return self['output'].asFloat()

    @output.setter
    def output(self, value: float) -> None:
        """
        Set the output value

        :param value: float, the output value
        """

        self['output'] = value


NodeRegistry()[Cos.nodeType()] = Cos
