from typing import Optional, Union

from maya.api import OpenMaya as om

from . import nodeLib


class DGNode(nodeLib.Node):

    def __init__(self, name: Union[str, om.MObject] = None) -> None:

        """
        Initialize an instance of DGNode

        Args:
            name: Optional[str], the name of the node
        """

        super().__init__(name=name)

    @property
    def isInteresting(self) -> bool:
        """
        Get the isHistoricallyInteresting value

        Returns:
            bool: the isHistoricallyInteresting value
        """

        return self['isHistoricallyInteresting'].asBool()

    @isInteresting.setter
    def isInteresting(self, value: bool) -> None:
        """
        Set the isHistoricallyInteresting value

        Returns:
            bool: the isHistoricallyInteresting value
        """

        self['isHistoricallyInteresting'] = value
