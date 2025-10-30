from typing import Optional, List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class Absolute(dgLib.DGNode):

    _NODE_TYPE = "absolute"
    _API_TYPE = om.MFn.kAbsolute

    @property
    def input(self) -> float:

        """
        Get the value of the input plug

        :return: float, the value of the input plug
        """

        return self['input'].asFloat()

    @input.setter
    def input(self, value: Union[float, om.MPlug]) -> None:

        """
        Set the value of the input plus

        :param value: float, The value to set the input to
        """
        self['input'] = value

    @property
    def output(self) -> float:

        """
        Get the value of the output plug

        :return: float, the value of the output plug
        """

        return self['output'].asFloat()


NodeRegistry()[Absolute.nodeType()] = Absolute
