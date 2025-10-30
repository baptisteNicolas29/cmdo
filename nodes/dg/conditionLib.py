from typing import List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class Condition(dgLib.DGNode):

    _NODE_TYPE = "condition"
    _API_TYPE = om.MFn.kCondition

    @property
    def firstTerm(self) -> float:
        
        """
        Get the firstTerm value

        :return: float, the firstTerm value
        """
        
        return self['firstTerm'].asFloat()
    
    @firstTerm.setter
    def firstTerm(self, value: float) -> None:
        
        """
        Set the firstTerm value

        :param value: float, the firstTerm value
        """
        
        self['firstTerm'] = value

    @property
    def secondTerm(self) -> float:
        
        """
        Get the secondTerm value

        :return: float, the secondTerm value
        """

        return self['secondTerm'].asFloat()

    @secondTerm.setter
    def secondTerm(self, value: float) -> None:
        
        """
        Set the secondTerm value

        :param value: float, the secondTerm value
        """

        self['secondTerm'] = value

    @property
    def operationList(self) -> List[str]:

        """
        Get the list of available operations

        :return: List[str], the list of available operations
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

        :return: int, the operation value
        """

        return self['operation'].asInt()

    @operation.setter
    def operation(self, value: Union[int, str]):

        """
        Set the operation value

        :param value: int | str, the operation to set, 
        either the index or the string (ie: "xyz")
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

        :return: List[float], the colorIfTrue value
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

        :param value: List[float], the colorIfTrue value
        """

        self['colorIfTrue'] = value

    @property
    def colorIfTrueR(self) -> float:
        """
        Get the colorIfTrueR value

        :return: float, the colorIfTrueR value
        """

        return self['colorIfTrueR'].asFloat()

    @colorIfTrueR.setter
    def colorIfTrueR(self, value: float) -> None:
        """
        Set the colorIfTrueR value

        :param value: float, the colorIfTrueR value
        """

        self['colorIfTrueR'] = value

    @property
    def colorIfTrueG(self) -> float:
        """
        Get the colorIfTrueG value

        :return: float, the colorIfTrueG value
        """

        return self['colorIfTrueG'].asFloat()

    @colorIfTrueG.setter
    def colorIfTrueG(self, value: float) -> None:
        """
        Set the colorIfTrueG value

        :param value: float, the colorIfTrueG value
        """

        self['colorIfTrueG'] = value

    @property
    def colorIfTrueB(self) -> float:
        """
        Get the colorIfTrueB value

        :return: float, the colorIfTrueB value
        """

        return self['colorIfTrueB'].asFloat()

    @colorIfTrueB.setter
    def colorIfTrueB(self, value: float) -> None:
        """
        Set the colorIfTrueB value

        :param value: float, the colorIfTrueB value
        """

        self['colorIfTrueB'] = value

    @property
    def colorIfFalse(self) -> List[float]:
        """
        Get the colorIfFalse value

        :return: List[float], the colorIfFalse value
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

        :param value: List[float], the colorIfFalse value
        """

        self['colorIfFalse'] = value

    @property
    def colorIfFalseR(self) -> float:
        """
        Get the colorIfFalseR value

        :return: float, the colorIfFalseR value
        """

        return self['colorIfFalseR'].asFloat()

    @colorIfFalseR.setter
    def colorIfFalseR(self, value: float) -> None:
        """
        Set the colorIfFalseR value

        :param value: float, the colorIfFalseR value
        """

        self['colorIfFalseR'] = value

    @property
    def colorIfFalseG(self) -> float:
        """
        Get the colorIfFalseG value

        :return: float, the colorIfFalseG value
        """

        return self['colorIfFalseG'].asFloat()

    @colorIfFalseG.setter
    def colorIfFalseG(self, value: float) -> None:
        """
        Set the colorIfFalseG value

        :param value: float, the colorIfFalseG value
        """

        self['colorIfFalseG'] = value

    @property
    def colorIfFalseB(self) -> float:
        """
        Get the colorIfFalseB value

        :return: float, the colorIfFalseB value
        """

        return self['colorIfFalseB'].asFloat()

    @colorIfFalseB.setter
    def colorIfFalseB(self, value: float) -> None:
        """
        Set the colorIfFalseB value

        :param value: float, the colorIfFalseB value
        """

        self['colorIfFalseB'] = value
    
    
NodeRegistry()[Condition.nodeType()] = Condition
