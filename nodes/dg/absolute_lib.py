from typing import Optional, List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dg_lib
from ...core.node_registry import NodeRegistry


class Absolute(dg_lib.DGNode):

    _NODE_TYPE = "absolute"
    _API_TYPE = om.MFn.kAbsolute

    def __init__(self, name: Union[str, om.MObject] = None) -> None:

        """
        Initialize an instance of Absolute

        Args:
            name: str | om.MObject, the name of the node
        """

        super().__init__(name=name)

    @property
    def input(self) -> float:

        """
        Get the value of the input plug

        Returns:
            float: the value of the input plug
        """

        return self['input'].asFloat()

    @input.setter
    def input(self, value: Union[float, om.MPlug]) -> None:

        """
        Set the value of the input plus

        Args:
            value (float): The value to set the input to
        """
        self['input'] = value

    @property
    def output(self) -> float:

        """
        Get the value of the output plug

        Returns:
            float: the value of the output plug
        """

        return self['output'].asFloat()


NodeRegistry()[Absolute.nodeType()] = Absolute
