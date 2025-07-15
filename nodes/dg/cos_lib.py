from maya.api import OpenMaya as om

from ...core.abstract import dg_lib
from ...core.node_registry import NodeRegistry


class Cos(dg_lib.DGNode):

    _NODE_TYPE = "cos"
    _API_TYPE = om.MFn.kCos

    def __init__(self, name: str | om.MObject = None) -> None:

        """
        Initialize an instance of Cos

        Args:
            name: str | om.MObject, the name of the node
        """

        super().__init__(name=name)

    @property
    def input(self) -> float:

        """
        Get the input value

        Returns:
            float: the input value
        """

        return self['input'].asFloat()

    @input.setter
    def input(self, value: float) -> None:
        
        """
        Set the input value

        Args:
            value: float, the input value
        """

        self['input'] = value

    @property
    def output(self) -> float:
        """
        Get the output value

        Returns:
            float: the output value
        """

        return self['output'].asFloat()

    @output.setter
    def output(self, value: float) -> None:
        """
        Set the output value

        Args:
            value: float, the output value
        """

        self['output'] = value


NodeRegistry()[Cos.nodeType()] = Cos
