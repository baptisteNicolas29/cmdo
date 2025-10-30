from typing import List

from maya import cmds
from maya.api import OpenMaya as om

from ...core.nodeRegistry import NodeRegistry
from ...core.abstract import dagLib


class Locator(dagLib.DAGNode):
    _NODE_TYPE = "locator"
    _API_TYPE = om.MFn.kLocator

    @property
    def localScale(self) -> List[float]:
        """
        Get the localScale values

        :return: List[float] the localScale values
        """
        
        return self['localScale'].value

    @localScale.setter
    def localScale(self, value: List[float]) -> None:
        """
        Set the localScale values

        :param value: List[float], the localScale values to set
        """
        
        self['localScale'] = value

    @property
    def localPosition(self) -> List[float]:
        """
        Get the localPosition values

        :return: List[float] the localPosition values
        """
        
        return self['localPosition'].value

    @localPosition.setter
    def localPosition(self, value: List[float]) -> None:
        """
        Set the localPosition values

        :param value: List[float], the localPosition values to set
        """
        
        self['localPosition'] = value

    @property
    def worldPosition(self) -> List[float]:
        """
        Set the worldPosition values

        :return: List[float], the worldPosition values to set
        """

        return self['worldPosition'][0].value

    @property
    def worldPositionX(self) -> float:
        """
        Set the worldPositionX values

        :return: float, the worldPositionX values to set
        """

        return self['worldPosition'][0]['worldPositionX'].asFloat()

    @property
    def worldPositionY(self) -> float:
        """
        Set the worldPositionY values

        :return: float, the worldPositionY values to set
        """

        return self['worldPosition'][0]['worldPositionY'].asFloat()

    @property
    def worldPositionZ(self) -> float:
        """
        Set the worldPositionZ values

        :return: float, the worldPositionZ values to set
        """

        return self['worldPosition'][0]['worldPositionZ'].asFloat()

    @property
    def center(self) -> List[float]:
        """
        Set the center values

        :return: List[float], the center values to set
        """

        return self['center'].value

    @property
    def centerX(self) -> float:
        """
        Set the centerX values

        :return: float, the centerX values to set
        """
        return self['center'][0]['boundingBoxCenterX'].asFloat()

    @property
    def centerY(self) -> float:
        """
        Set the centerY values

        :return: float, the centerY values to set
        """

        return self['center'][0]['boundingBoxCenterY'].asFloat()

    @property
    def centerZ(self) -> float:
        """
        Set the centerZ values

        :return: float, the centerZ values to set
        """

        return self['center'][0]['boundingBoxCenterZ'].asFloat()


NodeRegistry()[Locator.nodeType()] = Locator
