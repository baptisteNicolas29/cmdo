from typing import List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class QuatToEuler(dgLib.DGNode):

    _NODE_TYPE = "quatToEuler"
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

        :param value: Union[int, str], the rotate order to set, either the index or the
                string (ie: "xyz")
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
    def inputQuat(self) -> List[float]:
        """
        Get the inputQuat value

        :return: List[float], the inputQuat value
        """
        return [
            self.inputQuatX,
            self.inputQuatY,
            self.inputQuatZ,
            self.inputQuatW
        ]

    @inputQuat.setter
    def inputQuat(self, value: List[float]):
        """
        Set the inputQuat value

        :param value: List[float], the inputQuat value
        """

        self['inputQuat'] = value

    @property
    def inputQuatX(self) -> float:

        """
        Get the inputQuatX value

        :return: float, the inputQuatX value
        """

        return self['inputQuatX'].asFloat()

    @inputQuatX.setter
    def inputQuatX(self, value: float) -> None:

        """
        Set the inputQuatX value

        :param value: float, the inputQuatX value
        """

        self['inputQuatX'] = value

    @property
    def inputQuatY(self) -> float:

        """
        Get the inputQuatY value

        :return: float, the inputQuatY value
        """

        return self['inputQuatY'].asFloat()

    @inputQuatY.setter
    def inputQuatY(self, value: float) -> None:

        """
        Set the inputQuatY value

        :param value: float, the inputQuatY value
        """

        self['inputQuatY'] = value

    @property
    def inputQuatZ(self) -> float:

        """
        Get the inputQuatZ value

        :return: float, the inputQuatZ value
        """

        return self['inputQuatZ'].asFloat()

    @inputQuatZ.setter
    def inputQuatZ(self, value: float) -> None:

        """
        Set the inputQuatZ value

        :param value: float, the inputQuatZ value
        """

        self['inputQuatZ'] = value

    @property
    def inputQuatW(self) -> float:

        """
        Get the inputQuatW value

        :return: float, the inputQuatW value
        """

        return self['inputQuatW'].asFloat()

    @inputQuatW.setter
    def inputQuatW(self, value: float) -> None:

        """
        Set the inputQuatW value

        :param value: float, the inputQuatW value
        """

        self['inputQuatW'] = value

    @property
    def outputRotate(self) -> List[float]:
        """
        Get the outputRotate value

        :return: List[float] the outputRotate value
        """
        return [
            self.outputRotateX,
            self.outputRotateY,
            self.outputRotateZ
        ]

    @property
    def outputRotateX(self) -> float:
        """
        Get the outputRotateX value

        :return: float, the outputRotateX value
        """

        return self['outputRotateX'].asFloat()

    @property
    def outputRotateY(self) -> float:
        """
        Get the outputRotateY value

        :return: float, the outputRotateY value
        """

        return self['outputRotateY'].asFloat()

    @property
    def outputRotateZ(self) -> float:
        """
        Get the outputRotateZ value

        :return: float, the outputRotateZ value
        """

        return self['outputRotateZ'].asFloat()


NodeRegistry()[QuatToEuler.nodeType()] = QuatToEuler
