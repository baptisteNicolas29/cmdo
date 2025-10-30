from typing import List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class SetRange(dgLib.DGNode):

    _NODE_TYPE = "setRange"
    _API_TYPE = om.MFn.kSetRange

    @property
    def min(self) -> List[float]:
        """
        Get the min value

        :return: List[float], the min value
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

        :param value: List[float], the min value
        """

        self['min'] = value

    @property
    def minX(self) -> float:
        """
        Get the minX value

        :return: List[float], the minX value
        """

        return self['minX'].asFloat()

    @minX.setter
    def minX(self, value: float) -> None:
        """
        Set the minX value

        :param value: List[float], the minX value
        """

        self['minX'] = value

    @property
    def minY(self) -> float:
        """
        Get the minY value

        :return: List[float], the minY value
        """

        return self['minY'].asFloat()

    @minY.setter
    def minY(self, value: float) -> None:
        """
        Set the minY value

        :param value: List[float], the minY value
        """

        self['minY'] = value

    @property
    def minZ(self) -> float:
        """
        Get the minZ value

        :return: List[float], the minZ value
        """

        return self['minZ'].asFloat()

    @minZ.setter
    def minZ(self, value: float) -> None:
        """
        Set the minZ value

        :param value: List[float], the minZ value
        """

        self['minZ'] = value

    @property
    def max(self) -> List[float]:
        """
        Get the max value

        :return: List[float], the max value
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

        :param value: List[float], the max value
        """

        self['max'] = value

    @property
    def maxX(self) -> float:
        """
        Get the maxX value

        :return: List[float], the maxX value
        """

        return self['maxX'].asFloat()

    @maxX.setter
    def maxX(self, value: float) -> None:
        """
        Set the maxX value

        :param value: List[float], the maxX value
        """

        self['maxX'] = value

    @property
    def maxY(self) -> float:
        """
        Get the maxY value

        :return: List[float], the maxY value
        """

        return self['maxY'].asFloat()

    @maxY.setter
    def maxY(self, value: float) -> None:
        """
        Set the maxY value

        :param value: List[float], the maxY value
        """

        self['maxY'] = value

    @property
    def maxZ(self) -> float:
        """
        Get the maxZ value

        :return: List[float], the maxZ value
        """

        return self['maxZ'].asFloat()

    @maxZ.setter
    def maxZ(self, value: float) -> None:
        """
        Set the maxZ value

        :param value: List[float], the maxZ value
        """

        self['maxZ'] = value

    @property
    def oldMin(self) -> List[float]:
        """
        Get the oldMin value

        :return: List[float], the oldMin value
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

        :param value: List[float], the oldMin value
        """

        self['oldMin'] = value

    @property
    def oldMinX(self) -> float:
        """
        Get the oldMinX value

        :return: List[float], the oldMinX value
        """

        return self['oldMinX'].asFloat()

    @oldMinX.setter
    def oldMinX(self, value: float) -> None:
        """
        Set the oldMinX value

        :param value: List[float], the oldMinX value
        """

        self['oldMinX'] = value

    @property
    def oldMinY(self) -> float:
        """
        Get the oldMinY value

        :return: List[float], the oldMinY value
        """

        return self['oldMinY'].asFloat()

    @oldMinY.setter
    def oldMinY(self, value: float) -> None:
        """
        Set the oldMinY value

        :param value: List[float], the oldMinY value
        """

        self['oldMinY'] = value

    @property
    def oldMinZ(self) -> float:
        """
        Get the oldMinZ value

        :return: List[float], the oldMinZ value
        """

        return self['oldMinZ'].asFloat()

    @oldMinZ.setter
    def oldMinZ(self, value: float) -> None:
        """
        Set the oldMinZ value

        :param value: List[float], the oldMinZ value
        """

        self['oldMinZ'] = value

    @property
    def oldMax(self) -> List[float]:
        """
        Get the oldMax value

        :return: List[float], the oldMax value
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

        :param value: List[float], the oldMax value
        """

        self['oldMax'] = value

    @property
    def oldMaxX(self) -> float:
        """
        Get the oldMaxX value

        :return: List[float], the oldMaxX value
        """

        return self['oldMaxX'].asFloat()

    @oldMaxX.setter
    def oldMaxX(self, value: float) -> None:
        """
        Set the oldMaxX value

        :param value: List[float], the oldMaxX value
        """

        self['oldMaxX'] = value

    @property
    def oldMaxY(self) -> float:
        """
        Get the oldMaxY value

        :return: List[float], the oldMaxY value
        """

        return self['oldMaxY'].asFloat()

    @oldMaxY.setter
    def oldMaxY(self, value: float) -> None:
        """
        Set the oldMaxY value

        :param value: List[float], the oldMaxY value
        """

        self['oldMaxY'] = value

    @property
    def oldMaxZ(self) -> float:
        """
        Get the oldMaxZ value

        :return: List[float], the oldMaxZ value
        """

        return self['oldMaxZ'].asFloat()

    @oldMaxZ.setter
    def oldMaxZ(self, value: float) -> None:
        """
        Set the oldMaxZ value

        :param value: List[float], the oldMaxZ value
        """

        self['oldMaxZ'] = value

    @property
    def outValue(self) -> List[float]:
        """
        Get the outValue value

        :return: List[float], the outValue value
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

        :return: List[float], the outValueX value
        """

        return self['outValueX'].asFloat()

    @property
    def outValueY(self) -> float:
        """
        Get the outValueY value

        :return: List[float], the outValueY value
        """

        return self['outValueY'].asFloat()

    @property
    def outValueZ(self) -> float:
        """
        Get the outValueZ value

        :return: List[float], the outValueZ value
        """

        return self['outValueZ'].asFloat()


NodeRegistry()[SetRange.nodeType()] = SetRange
