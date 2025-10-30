from typing import Any, Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class Choice(dgLib.DGNode):

    _NODE_TYPE = "choice"
    _API_TYPE = om.MFn.kChoice

    @property
    def selector(self) -> int:

        """
        Get the selector value

        :return: int, the selector value
        """

        return self['selector'].value

    @selector.setter
    def selector(self, value: Union[int, om.MPlug]) -> None:

        """
        Set the selector value

        :param value: Union[int ,om.MPlug], the selector value
        """

        self['selector'] = value

    @property
    def output(self) -> Any:

        """
        Get the output value

        :return: Any, the output value
        """

        return self['output'].value

    @property
    def inputCount(self) -> int:
        """
        Get the number of input compound attributes (numElements)

        :return: int, the number of input compound attributes
        """

        return self['input'].numElements()

    def getInput(self, index: int) -> Any:

        """
        Get the input value from index

        :return: Any, the index of the input to get value from
        """

        return self['input'][index].value

    def setInput(self, index: int, value: Union[Any, om.MPlug]) -> None:

        """
        Set the input value from index

        :param index: int, the index of the input to set value from
        :param value: Any, the value to set
        """

        self['input'][index] = value


NodeRegistry()[Choice.nodeType()] = Choice
