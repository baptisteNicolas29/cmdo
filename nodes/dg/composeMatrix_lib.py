from typing import Optional, List, Union

from maya.api import OpenMaya as om

from ...core import convert
from ...core.abstract import dg_lib
from ...core.node_registry import NodeRegistry


class ComposeMatrix(dg_lib.DGNode):

    _NODE_TYPE = "composeMatrix"
    _API_TYPE = om.MFn.kComposeMatrix

    def __init__(self, name: str | om.MObject = None) -> None:

        """
        Initialize an instance of ComposeMatrix

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

        if isinstance(value, int) and 0 < value < len(self.rotateOrderList):
            self['inputRotateOrder'] = value

        elif isinstance(value, str) and value in self.rotateOrderList:
            self['inputRotateOrder'] = self.rotateOrderList.index(value)

        else:
            err_str = [f'{i} - {s}' for i, s in enumerate(self.rotateOrderList)]
            raise AttributeError(
                f'{self.name}: Rotate Order needs valid input, got {value}'
                f'\nNeeded int or string: {err_str}'
            )

    @property
    def useEulerRotation(self) -> int:
        """
        Get the useEulerRotation value

        Returns:
            int: the useEulerRotation value
        """

        return self['useEulerRotation'].asInt()

    @useEulerRotation.setter
    def useEulerRotation(self, value: bool):
        """
        Set the useEulerRotation value

        Args:
            value: int, the useEulerRotation value
        """

        self['useEulerRotation'] = value

    @property
    def inputTranslate(self) -> List[float]:
        
        """
        Get the inputTranslate value

        Returns:
            List[float]: the inputTranslate value
        """
        
        return [
            self.inputTranslateX,
            self.inputTranslateY,
            self.inputTranslateZ
        ]

    @inputTranslate.setter
    def inputTranslate(self, value: List[float]):
        
        """
        Set the inputTranslate value

        Args:
            value: List[float], the inputTranslate value
        """

        self['inputTranslate'] = value

    @property
    def inputTranslateX(self) -> float:
        
        """
        Get the inputTranslateX value

        Returns:
            float: the inputTranslateX value
        """

        return self['inputTranslateX'].asFloat()

    @inputTranslateX.setter
    def inputTranslateX(self, value: float) -> None:
        
        """
        Set the inputTranslateX value

        Args:
            value: float, the inputTranslateX value
        """

        self['inputTranslateX'] = value

    @property
    def inputTranslateY(self) -> float:
        """
        Get the inputTranslateY value

        Returns:
            float: the inputTranslateY value
        """

        return self['inputTranslateY'].asFloat()

    @inputTranslateY.setter
    def inputTranslateY(self, value: float) -> None:
        """
        Set the inputTranslateY value

        Args:
            value: float, the inputTranslateY value
        """

        self['inputTranslateY'] = value

    @property
    def inputTranslateZ(self) -> float:
        """
        Get the inputTranslateZ value

        Returns:
            float: the inputTranslateZ value
        """

        return self['inputTranslateZ'].asFloat()

    @inputTranslateZ.setter
    def inputTranslateZ(self, value: float) -> None:
        """
        Set the inputTranslateZ value

        Args:
            value: float, the inputTranslateZ value
        """

        self['inputTranslateZ'] = value

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
    def inputScale(self) -> List[float]:

        """
        Get the inputScale value

        Returns:
            List[float]: the inputScale value
        """

        return [
            self.inputScaleX,
            self.inputScaleY,
            self.inputScaleZ
        ]

    @inputScale.setter
    def inputScale(self, value: List[float]):
        """
        Set the inputScale value

        Args:
            value: List[float], the inputScale value
        """

        self['inputScale'] = value

    @property
    def inputScaleX(self) -> float:
        """
        Get the inputScaleX value

        Returns:
            List[float]: the inputScaleX value
        """

        return self['inputScaleX'].asFloat()

    @inputScaleX.setter
    def inputScaleX(self, value: float) -> None:
        """
        Set the inputScaleX value

        Args:
            value: List[float], the inputScaleX value
        """

        self['inputScaleX'] = value

    @property
    def inputScaleY(self) -> float:
        """
        Get the inputScaleY value

        Returns:
            List[float]: the inputScaleY value
        """

        return self['inputScaleY'].asFloat()

    @inputScaleY.setter
    def inputScaleY(self, value: float) -> None:
        """
        Set the inputScaleY value

        Args:
            value: List[float], the inputScaleY value
        """

        self['inputScaleY'] = value

    @property
    def inputScaleZ(self) -> float:
        """
        Get the inputScaleZ value

        Returns:
            List[float]: the inputScaleZ value
        """

        return self['inputScaleZ'].asFloat()

    @inputScaleZ.setter
    def inputScaleZ(self, value: float) -> None:
        """
        Set the inputScaleZ value

        Args:
            value: List[float], the inputScaleZ value
        """

        self['inputScaleZ'] = value

    @property
    def inputShear(self) -> List[float]:
        
        """
        Get the inputShear value

        Returns:
            List[float]: the inputShear value
        """
        
        return [
            self.inputShearX,
            self.inputShearY,
            self.inputShearZ
        ]

    @inputShear.setter
    def inputShear(self, value: List[float]) -> None:
        
        """
        Set the inputShear value

        Args:
            value: List[float], the inputShear value
        """

        self['inputShear'] = value

    @property
    def inputShearX(self) -> float:
        
        """
        Get the inputShearX value

        Returns:
            float: the inputShearX value
        """

        return self['inputShearX'].asFloat()

    @inputShearX.setter
    def inputShearX(self, value) -> None:
        
        """
        Set the inputShearX value

        Args:
            value: float, the inputShearX value
        """

        self['inputShearX'] = value

    @property
    def inputShearY(self) -> float:
        
        """
        Get the inputShearY value

        Returns:
            float: the inputShearY value
        """

        return self['inputShearY'].asFloat()

    @inputShearY.setter
    def inputShearY(self, value) -> None:
        
        """
        Set the inputShearY value

        Args:
            value: float, the inputShearY value
        """

        self['inputShearY'] = value

    @property
    def inputShearZ(self) -> float:
        
        """
        Get the inputShearZ value

        Returns:
            float: the inputShearZ value
        """

        return self['inputShearZ'].asFloat()

    @inputShearZ.setter
    def inputShearZ(self, value) -> None:
        
        """
        Set the inputShearZ value

        Args:
            value: float, the inputShearZ value
        """

        self['inputShearZ'] = value

    @property
    def inputQuat(self) -> List[float]:
        """
        Get the inputQuat value

        Returns:
            List[float]: the inputQuat value
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

        Args:
            value: List[float], the inputQuat value
        """

        self['inputQuat'] = value

    @property
    def inputQuatX(self) -> float:

        """
        Get the inputQuatX value

        Returns:
            float: the inputQuatX value
        """

        return self['inputQuatX'].asFloat()

    @inputQuatX.setter
    def inputQuatX(self, value: float) -> None:

        """
        Set the inputQuatX value

        Args:
            value: float, the inputQuatX value
        """

        self['inputQuatX'] = value

    @property
    def inputQuatY(self) -> float:

        """
        Get the inputQuatY value

        Returns:
            float: the inputQuatY value
        """

        return self['inputQuatY'].asFloat()

    @inputQuatY.setter
    def inputQuatY(self, value: float) -> None:

        """
        Set the inputQuatY value

        Args:
            value: float, the inputQuatY value
        """

        self['inputQuatY'] = value

    @property
    def inputQuatZ(self) -> float:

        """
        Get the inputQuatZ value

        Returns:
            float: the inputQuatZ value
        """

        return self['inputQuatZ'].asFloat()

    @inputQuatZ.setter
    def inputQuatZ(self, value: float) -> None:

        """
        Set the inputQuatZ value

        Args:
            value: float, the inputQuatZ value
        """

        self['inputQuatZ'] = value

    @property
    def inputQuatW(self) -> float:

        """
        Get the inputQuatW value

        Returns:
            float: the inputQuatW value
        """

        return self['inputQuatW'].asFloat()

    @inputQuatW.setter
    def inputQuatW(self, value: float) -> None:

        """
        Set the inputQuatW value

        Args:
            value: float, the inputQuatW value
        """

        self['inputQuatW'] = value

    @property
    def outputMatrix(self) -> List[float]:

        """
        Get the outputMatrix value

        Returns:
            List[float]: the outputMatrix value
        """

        return self['outputMatrix'].value


NodeRegistry()[ComposeMatrix.nodeType()] = ComposeMatrix
