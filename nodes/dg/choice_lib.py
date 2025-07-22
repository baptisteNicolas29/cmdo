from typing import Any, Union

from maya.api import OpenMaya as om

from ...core.abstract import dg_lib
from ...core.node_registry import NodeRegistry


class Choice(dg_lib.DGNode):

    _NODE_TYPE = "choice"
    _API_TYPE = om.MFn.kChoice

    def __init__(self, name: Union[str, om.MObject] = None) -> None:

        """
        Initialize an instance of Choice

        Args:
            name: str | om.MObject, the name of the node
        """

        super().__init__(name=name)

    @property
    def selector(self) -> int:

        """
        Get the selector value

        Returns:
            int: the selector value
        """

        return self['selector'].value

    @selector.setter
    def selector(self, value: Union[int, om.MPlug]) -> None:

        """
        Set the selector value

        Args:
            value: int | om.MPlug, the selector value
        """

        self['selector'] = value

    @property
    def output(self) -> Any:

        """
        Get the output value

        Returns:
            Any: the output value
        """

        return self['output'].value

    @property
    def inputCount(self) -> int:
        """
        Get the number of input compound attributes (numElements)

        Returns:
            int: the number of input compound attributes
        """

        return self['input'].numElements()

    def getInput(self, index: int) -> Any:

        """
        Get the input value from index

        Returns:
            Any: the index of the input to get value from
        """

        return self['input'][index].value

    def setInput(self, index: int, value: Union[Any, om.MPlug]) -> None:

        """
        Set the input value from index

        Args:
            index: int, the index of the input to set value from
            value: Any, the value to set
        """

        self['input'][index] = value


NodeRegistry()[Choice.nodeType()] = Choice
