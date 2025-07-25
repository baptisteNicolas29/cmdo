from typing import List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class MultiplyDivide(dgLib.DGNode):

    _NODE_TYPE = "multiplyDivide"
    _API_TYPE = om.MFn.kMultiplyDivide

    def __init__(self, name: Union[str, om.MObject] = None) -> None:
        """
        Initialize an instance of MultiplyDivide

        Args:
            name: str | om.MObject, the name of the node
        """

        super().__init__(name=name)

    @property
    def operationList(self) -> List[str]:

        """
        Get the list of available operations

        Returns:
            List[str]: the list of available operations
        """

        return ['No Operation', 'Multiply', 'Divide', 'Power']

    @property
    def operation(self) -> int:
        """
        Get the operation value

        Returns:
            int: the operation value
        """

        return self['operation'].asInt()

    @operation.setter
    def operation(self, value: Union[int, str]):

        """
        Set the operation value

        Args:
            value: int | str, the operation to set, either the index or the
                string (ie: "xyz")
        """

        if isinstance(value, int) and 0 < value < len(self.operationList):
            self['operation'] = value

        elif isinstance(value, str) and value in self.operationList:
            self['operation'] = self.operationList.index(value)

        else:
            err_str = [f'{i} - {s}' for i, s in enumerate(self.operationList)]
            raise AttributeError(
                f'{self.name}: Operation needs valid input, got {value}'
                f'\nNeeded int or string: {err_str}'
            )

    @property
    def input1(self) -> List[float]:
        """
        Get the input1 value

        Returns:
            List[float]: the input1 value
        """

        return [
            self.input1X,
            self.input1Y,
            self.input1Z
        ]

    @input1.setter
    def input1(self, value: List[float]) -> None:
        """
        Set the input1 value

        Args:
            value: List[float], the input1 value
        """

        self['input1'] = value

    @property
    def input1X(self) -> float:
        """
        Get the input1X value

        Returns:
            List[float]: the input1X value
        """

        return self['input1X'].asFloat()

    @input1X.setter
    def input1X(self, value: float) -> None:
        """
        Set the input1X value

        Args:
            value: List[float], the input1X value
        """

        self['input1X'] = value

    @property
    def input1Y(self) -> float:
        """
        Get the input1Y value

        Returns:
            List[float]: the input1Y value
        """

        return self['input1Y'].asFloat()

    @input1Y.setter
    def input1Y(self, value: float) -> None:
        """
        Set the input1Y value

        Args:
            value: List[float], the input1Y value
        """

        self['input1Y'] = value

    @property
    def input1Z(self) -> float:
        """
        Get the input1Z value

        Returns:
            List[float]: the input1Z value
        """

        return self['input1Z'].asFloat()

    @input1Z.setter
    def input1Z(self, value: float) -> None:
        """
        Set the input1Z value

        Args:
            value: List[float], the input1Z value
        """

        self['input1Z'] = value

    @property
    def input2(self) -> List[float]:
        """
        Get the input2 value

        Returns:
            List[float]: the input2 value
        """

        return [
            self.input2X,
            self.input2Y,
            self.input2Z
        ]

    @input2.setter
    def input2(self, value: List[float]) -> None:
        """
        Set the input2 value

        Args:
            value: List[float], the input2 value
        """

        self['input2'] = value

    @property
    def input2X(self) -> float:
        """
        Get the input2X value

        Returns:
            List[float]: the input2X value
        """

        return self['input2X'].asFloat()

    @input2X.setter
    def input2X(self, value: float) -> None:
        """
        Set the input2X value

        Args:
            value: List[float], the input2X value
        """

        self['input2X'] = value

    @property
    def input2Y(self) -> float:
        """
        Get the input2Y value

        Returns:
            List[float]: the input2Y value
        """

        return self['input2Y'].asFloat()

    @input2Y.setter
    def input2Y(self, value: float) -> None:
        """
        Set the input2Y value

        Args:
            value: List[float], the input2Y value
        """

        self['input2Y'] = value

    @property
    def input2Z(self) -> float:
        """
        Get the input2Z value

        Returns:
            List[float]: the input2Z value
        """

        return self['input2Z'].asFloat()

    @input2Z.setter
    def input2Z(self, value: float) -> None:
        """
        Set the input2Z value

        Args:
            value: List[float], the input2Z value
        """

        self['input2Z'] = value

    @property
    def output(self) -> List[float]:
        """
        Get the output value

        Returns:
            List[float]: the output value
        """

        return [
            self.outputX,
            self.outputY,
            self.outputZ
        ]

    @property
    def outputX(self) -> float:
        """
        Get the outputX value
    
        Returns:
            List[float]: the outputX value
        """
    
        return self['outputX'].asFloat()

    @property
    def outputY(self) -> float:
        """
        Get the outputY value
    
        Returns:
            List[float]: the outputY value
        """
    
        return self['outputY'].asFloat()

    @property
    def outputZ(self) -> float:
        """
        Get the outputZ value
    
        Returns:
            List[float]: the outputZ value
        """
    
        return self['outputZ'].asFloat()


NodeRegistry()[MultiplyDivide.nodeType()] = MultiplyDivide
