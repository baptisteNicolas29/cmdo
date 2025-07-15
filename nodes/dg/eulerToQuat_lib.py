from typing import Optional, List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dg_lib
from ...core.node_registry import NodeRegistry


class EulerToQuat(dg_lib.DGNode):

    _NODE_TYPE = "eulerToQuat"
    _API_TYPE = om.MFn.kPluginDependNode

    def __init__(self, name: str | om.MObject = None) -> None:
        """
        Initialize an instance of EulerToQuat

        Args:
            name: str | om.MObject, the name of the node
        """

        super().__init__(name=name)

    @property
    def rotateOrderList(self) -> List[str]:

        """
        Get the list of available Rotate Orders

        Returns:
            List[str]: the list of available rotate orders
        """

        return ['xyz', 'yzx', 'zxy', 'xzy', 'yxz', 'zyx']

    @property
    def inputRotateOrder(self) -> int:

        """
        Get the inputRotateOrder value

        Returns:
            int: the inputRotateOrder value
        """

        return self['inputRotateOrder'].asInt()

    @inputRotateOrder.setter
    def inputRotateOrder(self, value: int | str):

        """
        Set the inputRotateOrder value

        Args:
            value: int | str, the rotate order to set, either the index or the
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
    def inputRotate(self) -> List[float]:
        """
        Get the inputRotate value

        Returns:
            List[float]: the inputRotate value
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

        Args:
            value: List[float], the inputRotate value
        """

        self['inputRotate'] = value

    @property
    def inputRotateX(self) -> float:
        """
        Get the inputRotateX value

        Returns:
            float: the inputRotateX value
        """

        return self['inputRotateX'].asFloat()

    @inputRotateX.setter
    def inputRotateX(self, value: float) -> None:
        """
        Set the inputRotateX value

        Args:
            value: float, the inputRotateX value
        """

        self['inputRotateX'] = value

    @property
    def inputRotateY(self) -> float:
        """
        Get the inputRotateY value

        Returns:
            float: the inputRotateY value
        """

        return self['inputRotateY'].asFloat()

    @inputRotateY.setter
    def inputRotateY(self, value: float) -> None:
        """
        Set the inputRotateY value

        Args:
            value: float, the inputRotateY value
        """

        self['inputRotateY'] = value

    @property
    def inputRotateZ(self) -> float:
        """
        Get the inputRotateZ value

        Returns:
            float: the inputRotateZ value
        """

        return self['inputRotateZ'].asFloat()

    @inputRotateZ.setter
    def inputRotateZ(self, value: float) -> None:
        """
        Set the inputRotateZ value

        Args:
            value: float, the inputRotateZ value
        """

        self['inputRotateZ'] = value

    @property
    def outputQuat(self) -> List[float]:
        """
        Get the outputQuat value

        Returns:
            List[float]: the outputQuat value
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

        Returns:
            float: the outputQuatX value
        """

        return self['outputQuatX'].asFloat()

    @property
    def outputQuatY(self) -> float:

        """
        Get the outputQuatY value

        Returns:
            float: the outputQuatY value
        """

        return self['outputQuatY'].asFloat()

    @property
    def outputQuatZ(self) -> float:

        """
        Get the outputQuatZ value

        Returns:
            float: the outputQuatZ value
        """

        return self['outputQuatZ'].asFloat()

    @property
    def outputQuatW(self) -> float:

        """
        Get the outputQuatW value

        Returns:
            float: the outputQuatW value
        """

        return self['outputQuatW'].asFloat()


NodeRegistry()[EulerToQuat.nodeType()] = EulerToQuat
