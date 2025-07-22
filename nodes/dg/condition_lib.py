from typing import List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dg_lib
from ...core.node_registry import NodeRegistry


class Condition(dg_lib.DGNode):

    _NODE_TYPE = "condition"
    _API_TYPE = om.MFn.kCondition

    def __init__(self, name: Union[str, om.MObject] = None) -> None:

        """
        Initialize an instance of Condition

        Args:
            name: str | om.MObject, the name of the node
        """

        super().__init__(name=name)

    @property
    def firstTerm(self) -> float:
        
        """
        Get the firstTerm value

        Returns:
            float: the firstTerm value
        """
        
        return self['firstTerm'].asFloat()
    
    @firstTerm.setter
    def firstTerm(self, value: float) -> None:
        
        """
        Set the firstTerm value

        Args:
            value: float, the firstTerm value
        """
        
        self['firstTerm'] = value

    @property
    def secondTerm(self) -> float:
        
        """
        Get the secondTerm value

        Returns:
            float: the secondTerm value
        """

        return self['secondTerm'].asFloat()

    @secondTerm.setter
    def secondTerm(self, value: float) -> None:
        
        """
        Set the secondTerm value

        Args:
            value: float, the secondTerm value
        """

        self['secondTerm'] = value

    @property
    def operationList(self) -> List[str]:

        """
        Get the list of available operations

        Returns:
            List[str]: the list of available operations
        """

        return [
            'Equal', 'Not Equal',
            'Greater Than', 'Greater or Equal',
            'Less Than', 'Less or Equal'
        ]

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
    def colorIfTrue(self) -> List[float]:
        """
        Get the colorIfTrue value

        Returns:
            List[float]: the colorIfTrue value
        """

        return [
            self.colorIfTrueR,
            self.colorIfTrueG,
            self.colorIfTrueB
        ]

    @colorIfTrue.setter
    def colorIfTrue(self, value: List[float]):
        """
        Set the colorIfTrue value

        Args:
            value: List[float], the colorIfTrue value
        """

        self['colorIfTrue'] = value

    @property
    def colorIfTrueR(self) -> float:
        """
        Get the colorIfTrueR value

        Returns:
            float: the colorIfTrueR value
        """

        return self['colorIfTrueR'].asFloat()

    @colorIfTrueR.setter
    def colorIfTrueR(self, value: float) -> None:
        """
        Set the colorIfTrueR value

        Args:
            value: float, the colorIfTrueR value
        """

        self['colorIfTrueR'] = value

    @property
    def colorIfTrueG(self) -> float:
        """
        Get the colorIfTrueG value

        Returns:
            float: the colorIfTrueG value
        """

        return self['colorIfTrueG'].asFloat()

    @colorIfTrueG.setter
    def colorIfTrueG(self, value: float) -> None:
        """
        Set the colorIfTrueG value

        Args:
            value: float, the colorIfTrueG value
        """

        self['colorIfTrueG'] = value

    @property
    def colorIfTrueB(self) -> float:
        """
        Get the colorIfTrueB value

        Returns:
            float: the colorIfTrueB value
        """

        return self['colorIfTrueB'].asFloat()

    @colorIfTrueB.setter
    def colorIfTrueB(self, value: float) -> None:
        """
        Set the colorIfTrueB value

        Args:
            value: float, the colorIfTrueB value
        """

        self['colorIfTrueB'] = value

    @property
    def colorIfFalse(self) -> List[float]:
        """
        Get the colorIfFalse value

        Returns:
            List[float]: the colorIfFalse value
        """

        return [
            self.colorIfFalseR,
            self.colorIfFalseG,
            self.colorIfFalseB
        ]

    @colorIfFalse.setter
    def colorIfFalse(self, value: List[float]):
        """
        Set the colorIfFalse value

        Args:
            value: List[float], the colorIfFalse value
        """

        self['colorIfFalse'] = value

    @property
    def colorIfFalseR(self) -> float:
        """
        Get the colorIfFalseR value

        Returns:
            float: the colorIfFalseR value
        """

        return self['colorIfFalseR'].asFloat()

    @colorIfFalseR.setter
    def colorIfFalseR(self, value: float) -> None:
        """
        Set the colorIfFalseR value

        Args:
            value: float, the colorIfFalseR value
        """

        self['colorIfFalseR'] = value

    @property
    def colorIfFalseG(self) -> float:
        """
        Get the colorIfFalseG value

        Returns:
            float: the colorIfFalseG value
        """

        return self['colorIfFalseG'].asFloat()

    @colorIfFalseG.setter
    def colorIfFalseG(self, value: float) -> None:
        """
        Set the colorIfFalseG value

        Args:
            value: float, the colorIfFalseG value
        """

        self['colorIfFalseG'] = value

    @property
    def colorIfFalseB(self) -> float:
        """
        Get the colorIfFalseB value

        Returns:
            float: the colorIfFalseB value
        """

        return self['colorIfFalseB'].asFloat()

    @colorIfFalseB.setter
    def colorIfFalseB(self, value: float) -> None:
        """
        Set the colorIfFalseB value

        Args:
            value: float, the colorIfFalseB value
        """

        self['colorIfFalseB'] = value
    
    
NodeRegistry()[Condition.nodeType()] = Condition
