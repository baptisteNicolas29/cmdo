from typing import List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class DecomposeMatrix(dgLib.DGNode):

    _NODE_TYPE = "decomposeMatrix"
    _API_TYPE = om.MFn.kDecomposeMatrix

    def __init__(self, name: Union[str, om.MObject] = None) -> None:

        """
        Initialize an instance of DecomposeMatrix

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

    @property
    def inputMatrix(self) -> List[float]:
        """
        Get the inputMatrix value

        Returns:
            List[float]: the inputMatrix value
        """

        return self['inputMatrix'].value

    @inputMatrix.setter
    def inputMatrix(self, value: Union[List[float], om.MPlug]) -> None:
        """
        Set the inputMatrix value

        Args:
            value: List[float] | om.MPlug, the inputMatrix value
        """

        self['inputMatrix'] = value

    @property
    def outputTranslate(self) -> List[float]:

        """
        Get the outputTranslate value

        Returns:
            List[float]: the outputTranslate value
        """

        return [
            self.outputTranslateX,
            self.outputTranslateY,
            self.outputTranslateZ
        ]

    @property
    def outputTranslateX(self) -> float:

        """
        Get the outputTranslateX value

        Returns:
            float: the outputTranslateX value
        """

        return self['outputTranslateX'].asFloat()

    @property
    def outputTranslateY(self) -> float:
        """
        Get the outputTranslateY value

        Returns:
            float: the outputTranslateY value
        """

        return self['outputTranslateY'].asFloat()

    @property
    def outputTranslateZ(self) -> float:
        """
        Get the outputTranslateZ value

        Returns:
            float: the outputTranslateZ value
        """

        return self['outputTranslateZ'].asFloat()

    @property
    def outputRotate(self) -> List[float]:
        """
        Get the outputRotate value

        Returns:
            List[float]: the outputRotate value
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

        Returns:
            float: the outputRotateX value
        """

        return self['outputRotateX'].asFloat()

    @property
    def outputRotateY(self) -> float:
        """
        Get the outputRotateY value

        Returns:
            float: the outputRotateY value
        """

        return self['outputRotateY'].asFloat()

    @property
    def outputRotateZ(self) -> float:
        """
        Get the outputRotateZ value

        Returns:
            float: the outputRotateZ value
        """

        return self['outputRotateZ'].asFloat()

    @property
    def outputScale(self) -> List[float]:

        """
        Get the outputScale value

        Returns:
            List[float]: the outputScale value
        """

        return [
            self.outputScaleX,
            self.outputScaleY,
            self.outputScaleZ
        ]

    @property
    def outputScaleX(self) -> float:
        """
        Get the outputScaleX value

        Returns:
            List[float]: the outputScaleX value
        """

        return self['outputScaleX'].asFloat()

    @property
    def outputScaleY(self) -> float:
        """
        Get the outputScaleY value

        Returns:
            List[float]: the outputScaleY value
        """

        return self['outputScaleY'].asFloat()

    @property
    def outputScaleZ(self) -> float:
        """
        Get the outputScaleZ value

        Returns:
            List[float]: the outputScaleZ value
        """

        return self['outputScaleZ'].asFloat()

    @property
    def outputShear(self) -> List[float]:

        """
        Get the outputShear value

        Returns:
            List[float]: the outputShear value
        """

        return [
            self.outputShearX,
            self.outputShearY,
            self.outputShearZ
        ]

    @property
    def outputShearX(self) -> float:

        """
        Get the outputShearX value

        Returns:
            float: the outputShearX value
        """

        return self['outputShearX'].asFloat()

    @property
    def outputShearY(self) -> float:

        """
        Get the outputShearY value

        Returns:
            float: the outputShearY value
        """

        return self['outputShearY'].asFloat()

    @property
    def outputShearZ(self) -> float:

        """
        Get the outputShearZ value

        Returns:
            float: the outputShearZ value
        """

        return self['outputShearZ'].asFloat()

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


NodeRegistry()[DecomposeMatrix.nodeType()] = DecomposeMatrix
