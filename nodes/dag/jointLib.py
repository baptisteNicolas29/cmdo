from typing import Optional, Union, List

from maya import cmds
from maya.api import OpenMaya as om, OpenMayaAnim as oma

from ...core.cmdoTyping import CmdoObject
from ...core.nodeRegistry import NodeRegistry
from .transformLib import Transform


class Joint(Transform):

    _NODE_TYPE = "joint"
    _API_TYPE = om.MFn.kJoint

    @property
    def mfnIkJoint(self) -> oma.MFnIkJoint:
        """
        Get MFnIkJoint of the om.MObject

        :return: om.MFnIkJoint: the joint object
        """

        return oma.MFnIkJoint(self)

    @property
    def radius(self) -> float:

        """
        Get the joint radius

        :return: float: the radius of the joint
        """

        return self['radius'].asFloat()

    @radius.setter
    def radius(self, value: float) -> None:

        """
        Set the joint radius

        :param value: float, the value of the radius to set
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
        """
        Get the drawStyle value

        :return: int, the index of the drawStyle
        """

        return self['drawStyle'].asInt()

    @drawStyle.setter
    def drawStyle(self, value):
        self['drawStyle'] = value

    @property
    def segmentScaleCompensate(self) -> bool:

        """
        Get the segment scale compensate state

        :return: bool, if segment scale compensate is activated
        """

        return self["segmentScaleCompensate"].asBool()

    @segmentScaleCompensate.setter
    def segmentScaleCompensate(self, value: bool) -> None:

        """
        Set the segment scale compensate state

        :param value: bool, the value to set segment scale compensate to

        """

        self["segmentScaleCompensate"] = value

    @property
    def orientJointAxisList(self) -> List[str]:
        """

        :return:
        """

        return ['xyz', 'yzx', 'zxy', 'zyx', 'yxz', 'xzy', 'none']

    @property
    def orientJointSecondaryAxisList(self) -> List[str]:
        """

        :return:
        """

        return ['xup', 'xdown', 'yup', 'ydown', 'zup', 'zdown', 'none']

    # TODO: add orientJoint function
    def orientJointAxis(self, primAxis, secondAxis) -> None: ...


NodeRegistry()[Joint.nodeType()] = Joint
