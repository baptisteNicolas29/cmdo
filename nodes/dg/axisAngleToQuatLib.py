from typing import List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class AxisAngleToQuat(dgLib.DGNode):

    _NODE_TYPE = "axisAngleToQuat"
    _API_TYPE = om.MFn.kPluginDependNode

    @property
    def inputAngle(self) -> float:

        """
        Get the inputAngle value

        :return: float, the inputAngle value
        """

        return self['inputAngle'].asFloat()

    @inputAngle.setter
    def inputAngle(self, value: Union[float, om.MPlug]) -> None:
        """
        Set the inputAngle value

        :param value: float, the inputAngle value
        """

        self['inputAngle'] = value

    @property
    def inputAxis(self) -> float:
        """
        Get the inputAxis value

        :return: float, the inputAxis value
        """

        return self['inputAxis'].value

    @inputAxis.setter
    def inputAxis(self, value: Union[float, om.MPlug]) -> None:
        """
        Set the inputAxis value

        :param value: float, the inputAxis value
        """

        self['inputAxis'] = value

    @property
    def inputAxisX(self) -> float:
        """
        Get the inputAxisX value

        :return: float, the inputAxisX value
        """

        return self['inputAxisX'].value

    @inputAxisX.setter
    def inputAxisX(self, value: Union[float, om.MPlug]) -> None:
        """
        Set the inputAxisX value

        :param value: float, the inputAxisX value
        """

        self['inputAxisX'] = value

    @property
    def inputAxisY(self) -> float:
        """
        Get the inputAxisY value

        :return: float, the inputAxisY value
        """

        return self['inputAxisY'].value

    @inputAxisY.setter
    def inputAxisY(self, value: Union[float, om.MPlug]) -> None:
        """
        Set the inputAxisY value

        :param value: float, the inputAxisY value
        """

        self['inputAxisY'] = value

    @property
    def inputAxisZ(self) -> float:
        """
        Get the inputAxisZ value

        :return: float, the inputAxisZ value
        """

        return self['inputAxisZ'].value

    @inputAxisZ.setter
    def inputAxisZ(self, value: Union[float, om.MPlug]) -> None:
        """
        Set the inputAxisZ value

        :param value: float, the inputAxisZ value
        """

        self['inputAxisZ'] = value

    @property
    def outputQuat(self) -> List[float]:
        """
        Get the outputQuat value

        :return: float, the outputQuat value
        """

        return self['outputQuat'].value

    @property
    def outputQuatX(self) -> float:
        """
        Get the outputQuatX value

        :return: float, the outputQuatX value
        """

        return self['outputQuatX'].value

    @property
    def outputQuatY(self) -> float:
        """
        Get the outputQuatY value

        :return: float, the outputQuatY value
        """

        return self['outputQuatY'].value

    @property
    def outputQuatZ(self) -> float:
        """
        Get the outputQuatZ value

        :return: float, the outputQuatZ value
        """

        return self['outputQuatZ'].value

    @property
    def outputQuatW(self) -> float:
        """
        Get the outputQuatW value

        :return: float, the outputQuatW value
        """

        return self['outputQuatW'].value


NodeRegistry()[AxisAngleToQuat.nodeType()] = AxisAngleToQuat
