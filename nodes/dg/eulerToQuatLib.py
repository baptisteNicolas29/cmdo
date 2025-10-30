from typing import Optional, List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class EulerToQuat(dgLib.DGNode):

    _NODE_TYPE = "eulerToQuat"
    _API_TYPE = om.MFn.kPluginDependNode

    @property
    def rotateOrderList(self) -> List[str]:

        """
        Get the list of available Rotate Orders

        :return: List[str], the list of available rotate orders
        """

        return ['xyz', 'yzx', 'zxy', 'xzy', 'yxz', 'zyx']

    @property
    def inputRotateOrder(self) -> int:

        """
        Get the inputRotateOrder value

        :return: int, the inputRotateOrder value
        """

        return self['inputRotateOrder'].asInt()

    @inputRotateOrder.setter
    def inputRotateOrder(self, value: Union[int, str]):

        """
        Set the inputRotateOrder value

        :param value: Union[int, str], the rotate order to set, 
        either the index or the string (ie: "xyz")
        """

        if isinstance(value, int):
            self['inputRotateOrder'] = value

        elif isinstance(value, str) and value in self.rotateOrderList:
            self['inputRotateOrder'] = self.rotateOrderList.index(value)

        else:
            raise AttributeError(
                f'{self.name}: Rotate Order needs valid input, got {value}'
            )

    @property
    def inputRotate(self) -> List[float]:
        """
        Get the inputRotate value

        :return: List[float], the inputRotate value
        """
        return [
            self.inputRotateX,
            self.inputRotateY,
            self.inputRotateZ
        ]

    @inputRotate.setter
    def inputRotate(self, value: List[float]):
        """
        Set the inputRotate value

        :param value: List[float], the inputRotate value
        """

        self['inputRotate'] = value

    @property
    def inputRotateX(self) -> float:
        """
        Get the inputRotateX value

        :return: float, the inputRotateX value
        """

        return self['inputRotateX'].asFloat()

    @inputRotateX.setter
    def inputRotateX(self, value: float) -> None:
        """
        Set the inputRotateX value

        :param value: float, the inputRotateX value
        """

        self['inputRotateX'] = value

    @property
    def inputRotateY(self) -> float:
        """
        Get the inputRotateY value

        :return: float, the inputRotateY value
        """

        return self['inputRotateY'].asFloat()

    @inputRotateY.setter
    def inputRotateY(self, value: float) -> None:
        """
        Set the inputRotateY value

        :param value: float, the inputRotateY value
        """

        self['inputRotateY'] = value

    @property
    def inputRotateZ(self) -> float:
        """
        Get the inputRotateZ value

        :return: float, the inputRotateZ value
        """

        return self['inputRotateZ'].asFloat()

    @inputRotateZ.setter
    def inputRotateZ(self, value: float) -> None:
        """
        Set the inputRotateZ value

        :param value: float, the inputRotateZ value
        """

        self['inputRotateZ'] = value

    @property
    def outputQuat(self) -> List[float]:
        """
        Get the outputQuat value

        :return: List[float] the outputQuat value
        """
        return [
            self.outputQuatX,
            self.outputQuatY,
            self.outputQuatZ,
            self.outputQuatW
        ]

    @property
    def outputQuatX(self) -> float:

        """
        Get the outputQuatX value

        :return: float, the outputQuatX value
        """

        return self['outputQuatX'].asFloat()

    @property
    def outputQuatY(self) -> float:

        """
        Get the outputQuatY value

        :return: float, the outputQuatY value
        """

        return self['outputQuatY'].asFloat()

    @property
    def outputQuatZ(self) -> float:

        """
        Get the outputQuatZ value

        :return: float, the outputQuatZ value
        """

        return self['outputQuatZ'].asFloat()

    @property
    def outputQuatW(self) -> float:

        """
        Get the outputQuatW value

        :return: float, the outputQuatW value
        """

        return self['outputQuatW'].asFloat()


NodeRegistry()[EulerToQuat.nodeType()] = EulerToQuat
