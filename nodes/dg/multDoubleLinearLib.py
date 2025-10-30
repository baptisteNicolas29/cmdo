from typing import Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class MultDoubleLinear(dgLib.DGNode):

    _NODE_TYPE = "multDoubleLinear"
    _API_TYPE = om.MFn.kMultDoubleLinear

    @property
    def input1(self) -> float:
        """
        Get the value of the input1 plug

        :return: float the value of the input1 plug
        """

        return self['input1'].asFloat()

    @input1.setter
    def input1(self, value: Union[float, om.MPlug]) -> None:
        """
        Set the value of the input1 plug

        :param value: float, the value of the input1 plug
        """

        self['input1'] = value

    @property
    def input2(self) -> float:
        """
        Get the value of the input2 plug

        :return: float the value of the input2 plug
        """

        return self['input2'].asFloat()

    @input2.setter
    def input2(self, value: Union[float, om.MPlug]) -> None:
        """
        Set the value of the input2 plug

        :param value: float, the value of the input2 plug
        """

        self['input2'] = value

    @property
    def output(self) -> float:
        """
        Get the value of the output plug

        :return: float the value of the output plug
        """

        return self['output'].asFloat()


NodeRegistry()[MultDoubleLinear.nodeType()] = MultDoubleLinear
