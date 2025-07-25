from typing import Optional, List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class AddDoubleLinear(dgLib.DGNode):

    _NODE_TYPE = "addDoubleLinear"
    _API_TYPE = om.MFn.kAddDoubleLinear

    def __init__(self, name: Union[str, om.MObject] = None) -> None:

        """
        Initialize an instance of AddDoubleLinear

        Args:
            name: str | om.MObject, the name of the node
        """

        super().__init__(name=name)

    @property
    def input1(self) -> float:
        """
        Get the value of the input1 plug

        Returns:
            float: the value of the input1 plug
        """

        return self['input1'].asFloat()

    @input1.setter
    def input1(self, value: Union[float, om.MPlug]) -> None:
        """
        Set the value of the input1 plug

        Args:
            value: float, the value of the input1 plug
        """

        self['input1'] = value

    @property
    def input2(self) -> float:

        """
        Get the value of the input2 plug

        Returns:
            float: the value of the input2 plug
        """

        return self['input2'].asFloat()

    @input2.setter
    def input2(self, value: Union[float, om.MPlug]) -> None:
        """
        Set the value of the input2 plug

        Args:
            value: float, the value of the input2 plug
        """

        self['input2'] = value

    @property
    def output(self) -> Optional[float]:

        """
        Get the value of the output plug

        Returns:
            float: the value of the output plug
        """

        return self['output'].asFloat()


NodeRegistry()[AddDoubleLinear.nodeType()] = AddDoubleLinear
