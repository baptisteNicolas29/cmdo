from typing import Optional, Union, List

from maya import cmds as mc
from maya.api import OpenMaya as om

from ...core.nodeRegistry import NodeRegistry
from .transformLib import Transform


class Joint(Transform):

    _NODE_TYPE = "joint"
    _API_TYPE = om.MFn.kJoint

    def __init__(self, name: Union[str, om.MObject] = None) -> None:

        """
        Initialize an instance of Joint

        Args:
            name: str | om.MObject, the name of the node
        """

        super().__init__(name=name)

    @property
    def radius(self) -> float:

        """
        Get the joint radius

        Returns:
            float: the radius of the joint

        """

        return self['radius'].asFloat()

    @radius.setter
    def radius(self, value: float) -> None:

        """
        Set the joint radius

        Args:
            value: float, the value of the radius to set
        """

        self['radius'] = value

    @property
    def jointOrient(self) -> List[float]:
        """

        :return:
        """
        return [self.jointOrientX, self.jointOrientY, self.jointOrientZ]

    @jointOrient.setter
    def jointOrient(self, value):
        """

        :param value:
        :return:
        """

        self['jointOrient'] = value

    @property
    def jointOrientX(self) -> float:
        """

        :return:
        """

        return self['jointOrientX'].asFloat()

    @jointOrientX.setter
    def jointOrientX(self, value) -> None:
        """

        :return:
        """

        self['jointOrientX'] = value

    @property
    def jointOrientY(self) -> float:
        """

        :return:
        """

        return self['jointOrientY'].asFloat()

    @jointOrientY.setter
    def jointOrientY(self, value) -> None:
        """

        :return:
        """

        self['jointOrientY'] = value

    @property
    def jointOrientZ(self) -> float:
        """

        :return:
        """

        return self['jointOrientZ'].asFloat()

    @jointOrientZ.setter
    def jointOrientZ(self, value) -> None:
        """

        :return:
        """

        self['jointOrientZ'] = value

    @property
    def drawStyle(self):
        return self['drawStyle'].asInt()

    @drawStyle.setter
    def drawStyle(self, value):
        self['drawStyle'] = value

    @property
    def segmentScaleCompensate(self) -> bool:

        """
        Get the segment scale compensate state

        Returns:
            bool: if segment scale compensate is activated
        """

        return self["segmentScaleCompensate"].asBool()

    @segmentScaleCompensate.setter
    def segmentScaleCompensate(self, value: bool) -> None:

        """
        Set the segment scale compensate state

        Args:
            value: bool, the value to set segment scale compensate to

        """

        self["segmentScaleCompensate"] = value


NodeRegistry()[Joint.nodeType()] = Joint
