from typing import List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dg_lib
from ...core.node_registry import NodeRegistry


class SetRange(dg_lib.DGNode):

    _NODE_TYPE = "setRange"
    _API_TYPE = om.MFn.kSetRange

    def __init__(self, name: Union[str, om.MObject] = None) -> None:
        """
        Initialize an instance of SetRange

        Args:
            name: str | om.MObject, the name of the node
        """

        super().__init__(name=name)

    @property
    def min(self) -> List[float]:
        """
        Get the min value

        Returns:
            List[float]: the min value
        """

        return [
            self.minX,
            self.minY,
            self.minZ
        ]

    @min.setter
    def min(self, value: List[float]):
        """
        Set the min value

        Args:
            value: List[float], the min value
        """

        self['min'] = value

    @property
    def minX(self) -> float:
        """
        Get the minX value

        Returns:
            List[float]: the minX value
        """

        return self['minX'].asFloat()

    @minX.setter
    def minX(self, value: float) -> None:
        """
        Set the minX value

        Args:
            value: List[float], the minX value
        """

        self['minX'] = value

    @property
    def minY(self) -> float:
        """
        Get the minY value

        Returns:
            List[float]: the minY value
        """

        return self['minY'].asFloat()

    @minY.setter
    def minY(self, value: float) -> None:
        """
        Set the minY value

        Args:
            value: List[float], the minY value
        """

        self['minY'] = value

    @property
    def minZ(self) -> float:
        """
        Get the minZ value

        Returns:
            List[float]: the minZ value
        """

        return self['minZ'].asFloat()

    @minZ.setter
    def minZ(self, value: float) -> None:
        """
        Set the minZ value

        Args:
            value: List[float], the minZ value
        """

        self['minZ'] = value

    @property
    def max(self) -> List[float]:
        """
        Get the max value

        Returns:
            List[float]: the max value
        """

        return [
            self.maxX,
            self.maxY,
            self.maxZ
        ]

    @max.setter
    def max(self, value: List[float]):
        """
        Set the max value

        Args:
            value: List[float], the max value
        """

        self['max'] = value

    @property
    def maxX(self) -> float:
        """
        Get the maxX value

        Returns:
            List[float]: the maxX value
        """

        return self['maxX'].asFloat()

    @maxX.setter
    def maxX(self, value: float) -> None:
        """
        Set the maxX value

        Args:
            value: List[float], the maxX value
        """

        self['maxX'] = value

    @property
    def maxY(self) -> float:
        """
        Get the maxY value

        Returns:
            List[float]: the maxY value
        """

        return self['maxY'].asFloat()

    @maxY.setter
    def maxY(self, value: float) -> None:
        """
        Set the maxY value

        Args:
            value: List[float], the maxY value
        """

        self['maxY'] = value

    @property
    def maxZ(self) -> float:
        """
        Get the maxZ value

        Returns:
            List[float]: the maxZ value
        """

        return self['maxZ'].asFloat()

    @maxZ.setter
    def maxZ(self, value: float) -> None:
        """
        Set the maxZ value

        Args:
            value: List[float], the maxZ value
        """

        self['maxZ'] = value

    @property
    def oldMin(self) -> List[float]:
        """
        Get the oldMin value

        Returns:
            List[float]: the oldMin value
        """

        return [
            self.oldMinX,
            self.oldMinY,
            self.oldMinZ
        ]

    @oldMin.setter
    def oldMin(self, value: List[float]):
        """
        Set the oldMin value

        Args:
            value: List[float], the oldMin value
        """

        self['oldMin'] = value

    @property
    def oldMinX(self) -> float:
        """
        Get the oldMinX value

        Returns:
            List[float]: the oldMinX value
        """

        return self['oldMinX'].asFloat()

    @oldMinX.setter
    def oldMinX(self, value: float) -> None:
        """
        Set the oldMinX value

        Args:
            value: List[float], the oldMinX value
        """

        self['oldMinX'] = value

    @property
    def oldMinY(self) -> float:
        """
        Get the oldMinY value

        Returns:
            List[float]: the oldMinY value
        """

        return self['oldMinY'].asFloat()

    @oldMinY.setter
    def oldMinY(self, value: float) -> None:
        """
        Set the oldMinY value

        Args:
            value: List[float], the oldMinY value
        """

        self['oldMinY'] = value

    @property
    def oldMinZ(self) -> float:
        """
        Get the oldMinZ value

        Returns:
            List[float]: the oldMinZ value
        """

        return self['oldMinZ'].asFloat()

    @oldMinZ.setter
    def oldMinZ(self, value: float) -> None:
        """
        Set the oldMinZ value

        Args:
            value: List[float], the oldMinZ value
        """

        self['oldMinZ'] = value

    @property
    def oldMax(self) -> List[float]:
        """
        Get the oldMax value

        Returns:
            List[float]: the oldMax value
        """

        return [
            self.oldMaxX,
            self.oldMaxY,
            self.oldMaxZ
        ]

    @oldMax.setter
    def oldMax(self, value: List[float]):
        """
        Set the oldMax value

        Args:
            value: List[float], the oldMax value
        """

        self['oldMax'] = value

    @property
    def oldMaxX(self) -> float:
        """
        Get the oldMaxX value

        Returns:
            List[float]: the oldMaxX value
        """

        return self['oldMaxX'].asFloat()

    @oldMaxX.setter
    def oldMaxX(self, value: float) -> None:
        """
        Set the oldMaxX value

        Args:
            value: List[float], the oldMaxX value
        """

        self['oldMaxX'] = value

    @property
    def oldMaxY(self) -> float:
        """
        Get the oldMaxY value

        Returns:
            List[float]: the oldMaxY value
        """

        return self['oldMaxY'].asFloat()

    @oldMaxY.setter
    def oldMaxY(self, value: float) -> None:
        """
        Set the oldMaxY value

        Args:
            value: List[float], the oldMaxY value
        """

        self['oldMaxY'] = value

    @property
    def oldMaxZ(self) -> float:
        """
        Get the oldMaxZ value

        Returns:
            List[float]: the oldMaxZ value
        """

        return self['oldMaxZ'].asFloat()

    @oldMaxZ.setter
    def oldMaxZ(self, value: float) -> None:
        """
        Set the oldMaxZ value

        Args:
            value: List[float], the oldMaxZ value
        """

        self['oldMaxZ'] = value

    @property
    def outValue(self) -> List[float]:
        """
        Get the outValue value

        Returns:
            List[float]: the outValue value
        """

        return [
            self.outValueX,
            self.outValueY,
            self.outValueZ
        ]

    @property
    def outValueX(self) -> float:
        """
        Get the outValueX value

        Returns:
            List[float]: the outValueX value
        """

        return self['outValueX'].asFloat()

    @property
    def outValueY(self) -> float:
        """
        Get the outValueY value

        Returns:
            List[float]: the outValueY value
        """

        return self['outValueY'].asFloat()

    @property
    def outValueZ(self) -> float:
        """
        Get the outValueZ value

        Returns:
            List[float]: the outValueZ value
        """

        return self['outValueZ'].asFloat()


NodeRegistry()[SetRange.nodeType()] = SetRange
