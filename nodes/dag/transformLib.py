from typing import Optional, List, Union

from maya import cmds
from maya.api import OpenMaya as om

from ...core.exceptions import CmdoPlugException, CmdoException
from ...core.plugsLib import Plug
from ...core.abstract import dagLib
from ...core.nodeRegistry import NodeRegistry


class Transform(dagLib.DAGNode):

    _NODE_TYPE = "transform"
    _API_TYPE = om.MFn.kTransform

    @property
    def spaceList(self) -> List[str]:
        """
        Get the list of available Spaces

        :return: List,[str]: the list of available Spaces
        """

        return ['local', 'relative', 'world', 'custom']

    @property
    def mfnTransform(self) -> om.MFnTransform:
        """
        Return an omMFnTransform object

        :return: om.MFnTransform, the transform object
        """

        return om.MFnTransform(self)

    @property
    def transformAttributes(self) -> List[Plug]:
        """
        The transform attribute plugs of the current node

        AKA: translate, rotate, scale

        :returns: list[Plug], list of transform plugs (tx, ty, etc... )
        """
        
        return [
            self[f'{attr}{axis}']
            for axis in ['X', 'Y', 'Z']
            for attr in ['translate', 'rotate', 'scale']
        ]

    @property
    def rotateOrderList(self) -> List[str]:

        """
        Get the list of available Rotate Orders

        :return: List,[str]: the list of available rotate orders
        """

        return ['xyz', 'yzx', 'zxy', 'xzy', 'yxz', 'zyx']

    @property
    def translate(self) -> List[float]:

        """
        Get the translate value

        :return: List,[float]: the translate value
        """

        return [
            self.translateX,
            self.translateY,
            self.translateZ
        ]

    @translate.setter
    def translate(self, value: List[float]):

        """
        Set the translate value

        :param value: List[float], the translate value
        """

        self['translate'] = value

    @property
    def translateX(self) -> float:

        """
        Get the translateX value

        :return: float, the translateX value
        """

        return self['translateX'].asFloat()

    @translateX.setter
    def translateX(self, value: float) -> None:

        """
        Set the translateX value

        :param value: float, the translateX value
        """

        self['translateX'] = value

    @property
    def translateY(self) -> float:

        """
        Get the translateY value

        :return: float, the translateY value
        """

        return self['translateY'].asFloat()

    @translateY.setter
    def translateY(self, value: float) -> None:

        """
        Set the translateY value

        :param value: float, the translateY value
        """

        self['translateY'] = value

    @property
    def translateZ(self) -> float:

        """
        Get the translateZ value

        :return: float, the translateZ value
        """

        return self['translateZ'].asFloat()

    @translateZ.setter
    def translateZ(self, value: float) -> None:

        """
        Set the translateZ value

        :param value: float, the translateZ value
        """
        
        self['translateZ'] = value

    @property
    def rotate(self) -> List[float]:

        """
        Get the rotate value

        :return: List,[float]: the rotate value
        """

        return [
            self.rotateX,
            self.rotateY,
            self.rotateZ
        ]

    @rotate.setter
    def rotate(self, value: List[float]):

        """
        Set the rotate value

        :param value: List[float], the rotate value
        """

        rotation = [
            om.MAngle(v, om.MAngle.kDegrees).asRadians()
            for v in value
        ]

        self['rotate'] = rotation

    @property
    def rotateX(self) -> float:
        
        """
        Get the rotateX value

        :return: List,[float]: the rotateX value
        """

        return self['rotateX'].asMAngle().asDegrees()

    @rotateX.setter
    def rotateX(self, value) -> None:
        
        """
        Set the rotate value

        :param value: List[float], the rotate value
        """

        angle = om.MAngle(value).asRadians()

        self['rotateX'] = angle

    @property
    def rotateY(self) -> float:
        
        """
        Get the rotateY value

        :return: List,[float]: the rotateY value
        """

        return self['rotateY'].asMAngle().asDegrees()

    @rotateY.setter
    def rotateY(self, value) -> None:
        
        """
        Set the rotateY value

        :param value: List[float], the rotateY value
        """

        self['rotateY'] = om.MAngle(value).asRadians()

    @property
    def rotateZ(self) -> float:
        
        """
        Get the rotateZ value

        :return: List,[float]: the rotateZ value
        """

        return self['rotateZ'].asMAngle().asDegrees()

    @rotateZ.setter
    def rotateZ(self, value) -> None:
        
        """
        Set the rotateZ value

        :param value: List[float], the rotateZ value
        """

        self['rotateZ'] = om.MAngle(value).asRadians()

    @property
    def scale(self) -> List[float]:

        """
        Get the scale value

        :return: List,[float]: the scale value
        """

        return [
            self.scaleX,
            self.scaleY,
            self.scaleZ
        ]

    @scale.setter
    def scale(self, value):

        """
        Set the scale value

        :param value: List[float], the scale value
        """

        self['scale'] = value

    @property
    def scaleX(self) -> float:

        """
        Get the scaleX value

        :return: List,[float]: the scaleX value
        """

        return self['scaleX'].asFloat()

    @scaleX.setter
    def scaleX(self, value) -> None:

        """
        Set the scaleX value

        :param value: List[float], the scaleX value
        """

        self['scaleX'] = value

    @property
    def scaleY(self) -> float:

        """
        Get the scaleY value

        :return: List,[float]: the scaleY value
        """

        return self['scaleY'].asFloat()

    @scaleY.setter
    def scaleY(self, value) -> None:

        """
        Set the scaleY value

        :param value: List[float], the scaleY value
        """

        self['scaleY'] = value

    @property
    def scaleZ(self) -> float:

        """
        Get the scaleZ value

        :return: List,[float]: the scale value
        """

        return self['scaleZ'].asFloat()

    @scaleZ.setter
    def scaleZ(self, value) -> None:

        """
        Set the scaleZ value

        :param value: List[float], the scaleZ value
        """

        self['scaleZ'] = value

    @property
    def rotateOrder(self) -> int:
        """
        Get the current transforms rotate order

        :return: int, the chosen rotate order index
        """
        return self['rotateOrder'].asInt()

    @rotateOrder.setter
    def rotateOrder(self, value: Union[int, str]) -> None:
        """
        Set the current transform's rotate order

        :param value: int | str, the rotate order to set, either the index or
            the string (ie: "xyz")
        """
        if isinstance(value, int):
            self['rotateOrder'] = value

        elif isinstance(value, str) and value in self.rotateOrderList:
            self['rotateOrder'] = self.rotateOrderList.index(value)

    @property
    def transformationMatrix(self) -> om.MTransformationMatrix:
        """
        Return the world Matrix as a MTransformationMatrix

        :return: om.MTransformationMatrix, the world transformation matrix
        """
        return om.MTransformationMatrix(self.worldMatrix)

    def resetTransforms(self):
        """

        :return:
        """
        self.translate = [0, 0, 0]
        self.rotate = [0, 0, 0]
        self.scale = [1, 1, 1]

    def resetMatrixToOffsetParentMatrix(self, space: Union[str, int] = 'local', customSpace: om.MMatrix = '',  raiseOnError: bool = False) -> None:
        """
        Set the offset parent matrix with the current worldMatrix and
        reset the current matrix

        :param space: Union[str, int], in which space to reset transform and store in offsetParentMatrix.
            Potential choices are: ['local', 'relative', 'world', 'custom']
        :param customSpace: om.MMatrix, the custom matrix to reset relative to
        :param raiseOnError: bool, raise if the offsetParentMatrix is connected or locked

        """

        isdDest = self['offsetParentMatrix'].isDestination
        isLocked = self['offsetParentMatrix'].isLocked

        if raiseOnError and (isdDest or isLocked):
            raise CmdoPlugException(
                f'Cannot reset matrix to offsetParentMatrix for {self}, '
                'the offsetParentMatrix plug is already connected'
            )

        if isinstance(space, int):
            space = self.spaceList[space]

        match space:
            case 'local':
                self['offsetParentMatrix'] = self['matrix'].value

            case 'relative':
                self['offsetParentMatrix'] = (
                        self.worldMatrix * self.parentMatrix.inverse()
                )

            case 'world':
                self['offsetParentMatrix'] = self.worldMatrix

            case 'custom':
                if not isinstance(customSpace, (om.MMatrix, list)):
                    raise CmdoException(
                        f'Custom space needs to be of type '
                        f'maya.api.OpenMaya.MMatrix. '
                        f'Got: {repr(customSpace)}'
                    )

                if isinstance(customSpace, list):

                    if len(customSpace) != 16:
                        raise CmdoException(
                            f'Custom space list needs to be of length 16. '
                            f'Got: {len(customSpace)}'
                        )

                    customSpace = om.MMatrix(customSpace)

                self['offsetParentMatrix'] = (
                        self.worldMatrix * customSpace.inverse()
                )

        self.resetTransforms()


NodeRegistry()[Transform.nodeType()] = Transform
