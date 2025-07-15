from typing import Optional

from maya.api import OpenMaya as om

from . import node_lib


class DGNode(node_lib.Node):

    def __init__(self, name: Optional[str] = None) -> None:

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
