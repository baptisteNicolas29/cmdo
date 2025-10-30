from typing import List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class AimMatrix(dgLib.DGNode):

    _NODE_TYPE = "aimMatrix"
    _API_TYPE = om.MFn.kAimMatrix

    @property
    def inputMatrix(self) -> List[float]:

        """
        Get the inputMatrix value

        :return: List[float] the inputMatrix value
        """

        return self['inputMatrix'].value

    @inputMatrix.setter
    def inputMatrix(self, value: Union[List[float], om.MPlug]) -> None:

        """
        Set the inputMatrix value

        :param value: List[float]|om.MMatrix, the inputMatrix value
        """

        self['inputMatrix'] = value

    @property
    def primaryInputAxis(self) -> List[float]:

        """
        Get the primaryInputAxis value

        :return: List[float] the primaryInputAxis value
        """

        return self['primaryInputAxis'].value

    @primaryInputAxis.setter
    def primaryInputAxis(self, value: Union[List[float], om.MPlug]) -> None:

        """
        Set the primaryInputAxis value

        :param value: List[float], the primaryInputAxis value
        """

        self['primaryInputAxis'] = value

    @property
    def primaryInputAxisX(self) -> float:

        """
        Get the primaryInputAxisX value

        :return: List[float] the primaryInputAxisX value
        """

        return self['primaryInputAxisX'].asFloat()

    @primaryInputAxisX.setter
    def primaryInputAxisX(self, value: Union[List[float], om.MPlug]) -> None:

        """
        Set the primaryInputAxisX value

        :param value: List[float], the primaryInputAxisX value
        """

        self['primaryInputAxisX'] = value

    @property
    def primaryInputAxisY(self) -> float:

        """
        Get the primaryInputAxisY value

        :return: List[float] the primaryInputAxisY value
        """

        return self['primaryInputAxisY'].asFloat()

    @primaryInputAxisY.setter
    def primaryInputAxisY(self, value: Union[List[float], om.MPlug]) -> None:

        """
        Set the primaryInputAxisY value

        :param value: List[float], the primaryInputAxisY value
        """

        self['primaryInputAxisY'] = value

    @property
    def primaryInputAxisZ(self) -> float:

        """
        Get the primaryInputAxisZ value

        :return: List[float] the primaryInputAxisZ value
        """

        return self['primaryInputAxisZ'].asFloat()

    @primaryInputAxisZ.setter
    def primaryInputAxisZ(self, value: Union[List[float], om.MPlug]) -> None:

        """
        Set the primaryInputAxisZ value

        :param value: List[float], the primaryInputAxisZ value
        """

        self['primaryInputAxisZ'] = value

    @property
    def primaryMode(self) -> int:

        """
        Get the primaryMode value

        :return: int, the primaryMode value
        """

        return self['primaryMode'].asInt()

    @primaryMode.setter
    def primaryMode(self, value: Union[int, om.MPlug]) -> None:

        """
        Set the primaryMode value

        :param value: int, the primaryMode value
        """

        self['primaryMode'] = value

    @property
    def primaryTargetMatrix(self) -> List[float]:

        """
        Get the primaryTargetMatrix value

        :return: List[float] the primaryTargetMatrix value
        """

        return self['primaryTargetMatrix'].value

    @primaryTargetMatrix.setter
    def primaryTargetMatrix(self, value: Union[List[float], om.MPlug]) -> None:

        """
        Set the primaryTargetMatrix value

        :param value: List[float], the primaryTargetMatrix value
        """

        self['primaryTargetMatrix'] = value

    @property
    def secondaryInputAxis(self) -> List[float]:

        """
        Get the secondaryInputAxis value

        :return: List[float] the secondaryInputAxis value
        """

        return self['secondaryInputAxis'].value

    @secondaryInputAxis.setter
    def secondaryInputAxis(self, value: Union[List[float], om.MPlug]) -> None:

        """
        Set the secondaryInputAxis value

        :param value: List[float], the secondaryInputAxis value
        """

        self['secondaryInputAxis'] = value

    @property
    def secondaryInputAxisX(self) -> float:

        """
        Get the secondaryInputAxisX value

        :return: List[float] the secondaryInputAxisX value
        """

        return self['secondaryInputAxisX'].asFloat()

    @secondaryInputAxisX.setter
    def secondaryInputAxisX(self, value: Union[List[float], om.MPlug]) -> None:

        """
        Set the secondaryInputAxisX value

        :param value: List[float], the secondaryInputAxisX value
        """

        self['secondaryInputAxisX'] = value

    @property
    def secondaryInputAxisY(self) -> float:

        """
        Get the secondaryInputAxisY value

        :return: List[float] the secondaryInputAxisY value
        """

        return self['secondaryInputAxisY'].asFloat()

    @secondaryInputAxisY.setter
    def secondaryInputAxisY(self, value: Union[List[float], om.MPlug]) -> None:

        """
        Set the secondaryInputAxisY value

        :param value: List[float], the secondaryInputAxisY value
        """

        self['secondaryInputAxisY'] = value

    @property
    def secondaryInputAxisZ(self) -> float:

        """
        Get the secondaryInputAxisZ value

        :return: List[float] the secondaryInputAxisZ value
        """

        return self['secondaryInputAxisZ'].asFloat()

    @secondaryInputAxisZ.setter
    def secondaryInputAxisZ(self, value: Union[List[float], om.MPlug]) -> None:

        """
        Set the secondaryInputAxisZ value

        :param value: List[float], the secondaryInputAxisZ value
        """

        self['secondaryInputAxisZ'] = value

    @property
    def secondaryMode(self) -> int:

        """
        Get the secondaryMode value

        :return: int, the secondaryMode value
        """

        return self['secondaryMode'].asInt()

    @secondaryMode.setter
    def secondaryMode(self, value: Union[int, om.MPlug]) -> None:

        """
        Set the secondaryMode value

        :param value: int, the secondaryMode value
        """

        self['secondaryMode'] = value

    @property
    def secondaryTargetMatrix(self) -> List[float]:

        """
        Get the secondaryTargetMatrix value

        :return: List[float] the secondaryTargetMatrix value
        """

        return self['secondaryTargetMatrix'].value

    @secondaryTargetMatrix.setter
    def secondaryTargetMatrix(self, value: Union[List[float], om.MPlug]) -> None:

        """
        Set the secondaryTargetMatrix value

        :param value: List[float], the secondaryTargetMatrix value
        """

        self['secondaryTargetMatrix'] = value

    @property
    def preSpaceMatrix(self) -> List[float]:

        """
        Get the preSpaceMatrix value

        :return: List[float] the preSpaceMatrix value
        """

        return self['preSpaceMatrix'].value

    @preSpaceMatrix.setter
    def preSpaceMatrix(self, value: Union[List[float], om.MPlug]) -> None:
        """
        Get the preSpaceMatrix value

        :param value: List[float], the preSpaceMatrix value
        """

        self['preSpaceMatrix'] = value

    @property
    def postSpaceMatrix(self) -> List[float]:
        """
        Get the postSpaceMatrix value

        :return: List[float] the postSpaceMatrix value
        """

        return self['postSpaceMatrix'].value

    @postSpaceMatrix.setter
    def postSpaceMatrix(self, value: Union[List[float], om.MPlug]) -> None:
        """
        Get the postSpaceMatrix value

        :param value: List[float], the postSpaceMatrix value
        """

        self['postSpaceMatrix'] = value

    @property
    def outputMatrix(self) -> List[float]:

        """
        Get the outputMatrix value

        :return: List[float]: the outputMatrix value
        """

        return self['outputMatrix'].value


NodeRegistry()[AimMatrix.nodeType()] = AimMatrix
