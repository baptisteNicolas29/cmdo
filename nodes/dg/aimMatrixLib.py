from typing import List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class AimMatrix(dgLib.DGNode):

    _NODE_TYPE = "aimMatrix"
    _API_TYPE = om.MFn.kAimMatrix

    def __init__(self, name: Union[str, om.MObject] = None) -> None:

        """
        Initialize an instance of AimMatrix

        Args:
            name: str | om.MObject, the name of the node
        """

        super().__init__(name=name)

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
            value: List[float]|om.MMatrix, the inputMatrix value
        """

        self['inputMatrix'] = value

    @property
    def primaryInputAxis(self) -> List[float]:

        """
        Get the primaryInputAxis value

        Returns:
            List[float]: the primaryInputAxis value
        """

        return self['primaryInputAxis'].value

    @primaryInputAxis.setter
    def primaryInputAxis(self, value: Union[List[float], om.MPlug]) -> None:

        """
        Set the primaryInputAxis value

        Args:
            value: List[float], the primaryInputAxis value
        """

        self['primaryInputAxis'] = value

    @property
    def primaryInputAxisX(self) -> float:

        """
        Get the primaryInputAxisX value

        Returns:
            List[float]: the primaryInputAxisX value
        """

        return self['primaryInputAxisX'].asFloat()

    @primaryInputAxisX.setter
    def primaryInputAxisX(self, value: Union[List[float], om.MPlug]) -> None:

        """
        Set the primaryInputAxisX value

        Args:
            value: List[float], the primaryInputAxisX value
        """

        self['primaryInputAxisX'] = value

    @property
    def primaryInputAxisY(self) -> float:

        """
        Get the primaryInputAxisY value

        Returns:
            List[float]: the primaryInputAxisY value
        """

        return self['primaryInputAxisY'].asFloat()

    @primaryInputAxisY.setter
    def primaryInputAxisY(self, value: Union[List[float], om.MPlug]) -> None:

        """
        Set the primaryInputAxisY value

        Args:
            value: List[float], the primaryInputAxisY value
        """

        self['primaryInputAxisY'] = value

    @property
    def primaryInputAxisZ(self) -> float:

        """
        Get the primaryInputAxisZ value

        Returns:
            List[float]: the primaryInputAxisZ value
        """

        return self['primaryInputAxisZ'].asFloat()

    @primaryInputAxisZ.setter
    def primaryInputAxisZ(self, value: Union[List[float], om.MPlug]) -> None:

        """
        Set the primaryInputAxisZ value

        Args:
            value: List[float], the primaryInputAxisZ value
        """

        self['primaryInputAxisZ'] = value

    @property
    def primaryMode(self) -> int:

        """
        Get the primaryMode value

        Returns:
            int: the primaryMode value
        """

        return self['primaryMode'].asInt()

    @primaryMode.setter
    def primaryMode(self, value: Union[int, om.MPlug]) -> None:

        """
        Set the primaryMode value

        Args:
            value: int, the primaryMode value
        """

        self['primaryMode'] = value

    @property
    def primaryTargetMatrix(self) -> List[float]:

        """
        Get the primaryTargetMatrix value

        Returns:
            List[float]: the primaryTargetMatrix value
        """

        return self['primaryTargetMatrix'].value

    @primaryTargetMatrix.setter
    def primaryTargetMatrix(self, value: Union[List[float], om.MPlug]) -> None:

        """
        Set the primaryTargetMatrix value

        Args:
            value: List[float], the primaryTargetMatrix value
        """

        self['primaryTargetMatrix'] = value

    @property
    def secondaryInputAxis(self) -> List[float]:

        """
        Get the secondaryInputAxis value

        Returns:
            List[float]: the secondaryInputAxis value
        """

        return self['secondaryInputAxis'].value

    @secondaryInputAxis.setter
    def secondaryInputAxis(self, value: Union[List[float], om.MPlug]) -> None:

        """
        Set the secondaryInputAxis value

        Args:
            value: List[float], the secondaryInputAxis value
        """

        self['secondaryInputAxis'] = value

    @property
    def secondaryInputAxisX(self) -> float:

        """
        Get the secondaryInputAxisX value

        Returns:
            List[float]: the secondaryInputAxisX value
        """

        return self['secondaryInputAxisX'].asFloat()

    @secondaryInputAxisX.setter
    def secondaryInputAxisX(self, value: Union[List[float], om.MPlug]) -> None:

        """
        Set the secondaryInputAxisX value

        Args:
            value: List[float], the secondaryInputAxisX value
        """

        self['secondaryInputAxisX'] = value

    @property
    def secondaryInputAxisY(self) -> float:

        """
        Get the secondaryInputAxisY value

        Returns:
            List[float]: the secondaryInputAxisY value
        """

        return self['secondaryInputAxisY'].asFloat()

    @secondaryInputAxisY.setter
    def secondaryInputAxisY(self, value: Union[List[float], om.MPlug]) -> None:

        """
        Set the secondaryInputAxisY value

        Args:
            value: List[float], the secondaryInputAxisY value
        """

        self['secondaryInputAxisY'] = value

    @property
    def secondaryInputAxisZ(self) -> float:

        """
        Get the secondaryInputAxisZ value

        Returns:
            List[float]: the secondaryInputAxisZ value
        """

        return self['secondaryInputAxisZ'].asFloat()

    @secondaryInputAxisZ.setter
    def secondaryInputAxisZ(self, value: Union[List[float], om.MPlug]) -> None:

        """
        Set the secondaryInputAxisZ value

        Args:
            value: List[float], the secondaryInputAxisZ value
        """

        self['secondaryInputAxisZ'] = value

    @property
    def secondaryMode(self) -> int:

        """
        Get the secondaryMode value

        Returns:
            int: the secondaryMode value
        """

        return self['secondaryMode'].asInt()

    @secondaryMode.setter
    def secondaryMode(self, value: Union[int, om.MPlug]) -> None:

        """
        Set the secondaryMode value

        Args:
            value: int, the secondaryMode value
        """

        self['secondaryMode'] = value

    @property
    def secondaryTargetMatrix(self) -> List[float]:

        """
        Get the secondaryTargetMatrix value

        Returns:
            List[float]: the secondaryTargetMatrix value
        """

        return self['secondaryTargetMatrix'].value

    @secondaryTargetMatrix.setter
    def secondaryTargetMatrix(self, value: Union[List[float], om.MPlug]) -> None:

        """
        Set the secondaryTargetMatrix value

        Args:
            value: List[float], the secondaryTargetMatrix value
        """

        self['secondaryTargetMatrix'] = value

    @property
    def preSpaceMatrix(self) -> List[float]:

        """
        Get the preSpaceMatrix value

        Returns:
            List[float]: the preSpaceMatrix value
        """

        return self['preSpaceMatrix'].value

    @preSpaceMatrix.setter
    def preSpaceMatrix(self, value: Union[List[float], om.MPlug]) -> None:
        """
        Get the preSpaceMatrix value

        Args:
            value: List[float], the preSpaceMatrix value
        """

        self['preSpaceMatrix'] = value

    @property
    def postSpaceMatrix(self) -> List[float]:
        """
        Get the postSpaceMatrix value

        Returns:
            List[float]: the postSpaceMatrix value
        """

        return self['postSpaceMatrix'].value

    @postSpaceMatrix.setter
    def postSpaceMatrix(self, value: Union[List[float], om.MPlug]) -> None:
        """
        Get the postSpaceMatrix value

        Args:
            value: List[float], the postSpaceMatrix value
        """

        self['postSpaceMatrix'] = value

    @property
    def outputMatrix(self) -> List[float]:

        """
        Get the outputMatrix value

        Returns:
            Liar[float]: the outputMatrix value
        """

        return self['outputMatrix'].value


NodeRegistry()[AimMatrix.nodeType()] = AimMatrix
