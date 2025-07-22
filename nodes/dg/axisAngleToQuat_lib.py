from typing import List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dg_lib
from ...core.node_registry import NodeRegistry


class AxisAngleToQuat(dg_lib.DGNode):

    _NODE_TYPE = "axisAngleToQuat"
    _API_TYPE = om.MFn.kPluginDependNode

    def __init__(self, name: Union[str, om.MObject] = None) -> None:

        """
        Initialize an instance of AxisAngleToQuat

        Args:
            name: str | om.MObject, the name of the node
        """

        super().__init__(name=name)

    @property
    def inputAngle(self) -> float:

        """
        Get the inputAngle value

        Returns:
             float: the inputAngle value
        """

        return self['inputAngle'].asFloat()

    @inputAngle.setter
    def inputAngle(self, value: Union[float, om.MPlug]) -> None:
        """
        Set the inputAngle value

        Args:
             value: float, the inputAngle value
        """

        self['inputAngle'] = value

    @property
    def inputAxis(self) -> float:
        """
        Get the inputAxis value

        Returns:
             float: the inputAxis value
        """

        return self['inputAxis'].value

    @inputAxis.setter
    def inputAxis(self, value: Union[float, om.MPlug]) -> None:
        """
        Set the inputAxis value

        Args:
             value: float, the inputAxis value
        """

        self['inputAxis'] = value

    @property
    def inputAxisX(self) -> float:
        """
        Get the inputAxisX value

        Returns:
             float: the inputAxisX value
        """

        return self['inputAxisX'].value

    @inputAxisX.setter
    def inputAxisX(self, value: Union[float, om.MPlug]) -> None:
        """
        Set the inputAxisX value

        Args:
             value: float, the inputAxisX value
        """

        self['inputAxisX'] = value

    @property
    def inputAxisY(self) -> float:
        """
        Get the inputAxisY value

        Returns:
             float: the inputAxisY value
        """

        return self['inputAxisY'].value

    @inputAxisY.setter
    def inputAxisY(self, value: Union[float, om.MPlug]) -> None:
        """
        Set the inputAxisY value

        Args:
             value: float, the inputAxisY value
        """

        self['inputAxisY'] = value

    @property
    def inputAxisZ(self) -> float:
        """
        Get the inputAxisZ value

        Returns:
             float: the inputAxisZ value
        """

        return self['inputAxisZ'].value

    @inputAxisZ.setter
    def inputAxisZ(self, value: Union[float, om.MPlug]) -> None:
        """
        Set the inputAxisZ value

        Args:
             value: float, the inputAxisZ value
        """

        self['inputAxisZ'] = value

    @property
    def outputQuat(self) -> List[float]:
        """
        Get the outputQuat value

        Returns:
             float: the outputQuat value
        """

        return self['outputQuat'].value

    @property
    def outputQuatX(self) -> float:
        """
        Get the outputQuatX value

        Returns:
             float: the outputQuatX value
        """

        return self['outputQuatX'].value

    @property
    def outputQuatY(self) -> float:
        """
        Get the outputQuatY value

        Returns:
             float: the outputQuatY value
        """

        return self['outputQuatY'].value

    @property
    def outputQuatZ(self) -> float:
        """
        Get the outputQuatZ value

        Returns:
             float: the outputQuatZ value
        """

        return self['outputQuatZ'].value

    @property
    def outputQuatW(self) -> float:
        """
        Get the outputQuatW value

        Returns:
             float: the outputQuatW value
        """

        return self['outputQuatW'].value


NodeRegistry()[AxisAngleToQuat.nodeType()] = AxisAngleToQuat
