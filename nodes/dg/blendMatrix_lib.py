from typing import List

from maya.api import OpenMaya as om

from ...core.abstract import dg_lib
from ...core.node_registry import NodeRegistry


class BlendMatrix(dg_lib.DGNode):

    _NODE_TYPE = "blendMatrix"
    _API_TYPE = om.MFn.kBlendMatrix

    def __init__(self, name: str | om.MObject = None) -> None:

        """
        Initialize an instance of BlendMatrix

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
    def inputMatrix(self, value: List[float] | om.MPlug) -> None:

        """
        Set the inputMatrix value

        Args:
            value: List[float] | om.MPlug, the inputMatrix value
        """

        self['inputMatrix'] = value

    @property
    def targetCount(self) -> int:

        """
        Get the number of target compound attributes (numElements)

        Returns:
            int: the number of target compound attributes
        """

        return self['target'].numElements()

    @property
    def outputMatrix(self) -> List[float]:

        """
        Get the outputMatrix value

        Returns:
            List[float]: the outputMatrix value
        """

        return self['outputMatrix'].value

    def getTargetMatrix(self, index: int) -> List[float]:
        """
        Get the targetMatrix from a target index value

        Args:
            index: int, the index of the target to get value from

        Returns:
            List[float]: the targetMatrix value
        """

        return self['target'][index]['targetMatrix'].value

    def setTargetMatrix(self, index: int, value: List[float] | om.MPlug) -> None:
        """
        Set the targetMatrix from a target index value

        Args:
            index: int, the index of the target to get value from
            value: List[float], the targetMatrix value
        """

        self['target'][index]['targetMatrix'] = value

    def getTargetUseMatrix(self, index: int) -> bool:
        """
        Get the targetUseMatrix from a target index value

        Args:
            index: int, the index of the target to get value from

        Returns:
            List[float]: the targetUseMatrix value
        """

        return self['target'][index]['useMatrix'].asBool()

    def setTargetUseMatrix(self, index: int, value: bool | om.MPlug) -> None:
        """
        Set the targetUseMatrix from a target index value

        Args:
            index: int, the index of the target to get value from
            value: List[float], the targetUseMatrix value
        """

        self['target'][index]['useMatrix'] = value

    def getTargetWeight(self, index: int) -> float:
        """
        Get the targetWeight from a target index value

        Args:
            index: int, the index of the target to get value from

        Returns:
            List[float]: the targetWeight value
        """

        return self['target'][index]['weight'].asFloat()

    def setTargetWeight(self, index: int, value: float | om.MPlug) -> None:
        """
        Set the targetWeight from a target index value

        Args:
            index: int, the index of the target to get value from
            value: List[float], the targetWeight value
        """

        self['target'][index]['weight'] = value

    def getTargetScaleWeight(self, index: int) -> float:
        """
        Get the targetScaleWeight from a target index value

        Args:
            index: int, the index of the target to get value from

        Returns:
            List[float]: the targetScaleWeight value
        """

        return self['target'][index]['scaleWeight'].asFloat()

    def setTargetScaleWeight(self, index: int, value: float | om.MPlug) -> None:
        """
        Set the targetScaleWeight from a target index value

        Args:
            index: int, the index of the target to get value from
            value: List[float], the targetScaleWeight value
        """

        self['target'][index]['scaleWeight'] = value
        
    def getTargetTranslateWeight(self, index: int) -> float:
        """
        Get the targetTranslateWeight from a target index value

        Args:
            index: int, the index of the target to get value from

        Returns:
            List[float]: the targetTranslateWeight value
        """

        return self['target'][index]['translateWeight'].asFloat()

    def setTargetTranslateWeight(self, index: int, value: float | om.MPlug) -> None:
        """
        Set the targetTranslateWeight from a target index value

        Args:
            index: int, the index of the target to get value from
            value: List[float], the targetTranslateWeight value
        """

        self['target'][index]['translateWeight'] = value

    def getTargetRotateWeight(self, index: int) -> float:
        """
        Get the targetRotateWeight from a target index value

        Args:
            index: int, the index of the target to get value from

        Returns:
            List[float]: the targetRotateWeight value
        """

        return self['target'][index]['rotateWeight'].asFloat()

    def setTargetRotateWeight(self, index: int, value: float | om.MPlug) -> None:
        """
        Set the targetRotateWeight from a target index value

        Args:
            index: int, the index of the target to get value from
            value: List[float], the targetRotateWeight value
        """

        self['target'][index]['rotateWeight'] = value

    def getTargetShearWeight(self, index: int) -> float:
        """
        Get the targetShearWeight from a target index value

        Args:
            index: int, the index of the target to get value from

        Returns:
            List[float]: the targetShearWeight value
        """

        return self['target'][index]['shearWeight'].asFloat()

    def setTargetShearWeight(self, index: int, value: float | om.MPlug) -> None:
        """
        Set the targetShearWeight from a target index value

        Args:
            index: int, the index of the target to get value from
            value: List[float], the targetShearWeight value
        """

        self['target'][index]['shearWeight'] = value


NodeRegistry()[BlendMatrix.nodeType()] = BlendMatrix
