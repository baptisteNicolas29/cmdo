from typing import List

from maya.api import OpenMaya as om

from ...core.abstract import dg_lib
from ...core.node_registry import NodeRegistry


class Sin(dg_lib.DGNode):

    _NODE_TYPE = "sin"
    _API_TYPE = om.MFn.kSin

    def __init__(self, name: str = None) -> None:

        """
        Initialize an instance of Sin

        Args:
            name: str, the name of the node
        """

        super().__init__(name=name)

    @property
    def input(self) -> List[float]:
        """
        Get the input value

        Returns:
            List[float]: the input value
        """

        return self['input'].asFloat()

    @input.setter
    def input(self, value: List[float]):
        """
        Set the input value

        Args:
            value: List[float], the input value
        """

        self['input'] = value

    @property
    def output(self) -> List[float]:
        """
        Get the output value

        Returns:
            List[float]: the output value
        """

        return self['output'].asFloat()

    @output.setter
    def output(self, value: List[float]):
        """
        Set the output value

        Args:
            value: List[float], the output value
        """

        self['output'] = value


NodeRegistry()[Sin.nodeType()] = Sin
