from typing import Optional, List, Union

from maya import cmds as mc
from maya.api import OpenMaya as om

from ...core.plugsLib import Plug
from ...core.abstract import dagLib
from ...core.nodeRegistry import NodeRegistry


class Transform(dagLib.DAGNode):

    _NODE_TYPE = "transform"
    _API_TYPE = om.MFn.kTransform

    def __init__(self, name: str = None, *args, **kwargs) -> None:

        """
        Initialize an instance of Transform

        Args:
            name: str | om.MObject, the name of the node
        """

        super().__init__(name=name)

    @property
    def mfnTransform(self) -> Optional[om.MFnTransform]:

        """
        Return an MFnTransform object

        Returns:
            MFnTransform: MFnTransform object
        """

        return om.MFnTransform(self)

    @property
    def transformAttributes(self) -> List[Plug]:
        """
        The transform attribute plugs of the current node
        AKA: translate, rotate, scale

        Returns:
            list[Plug]: list of transform plugs (tx, ty, etc... )
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

        Returns:
            List[str]: the list of available rotate orders
        """

        return ['xyz', 'yzx', 'zxy', 'xzy', 'yxz', 'zyx']

    @property
    def translate(self) -> List[float]:

        """
        Get the translate value

        Returns:
            List[float]: the translate value
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

        Args:
            value: List[float], the translate value
        """

        self['translate'] = value

    @property
    def translateX(self) -> float:

        """
        Get the translateX value

        Returns:
            float: the translateX value
        """

        return self['translateX'].asFloat()

    @translateX.setter
    def translateX(self, value: float) -> None:

        """
        Set the translateX value

        Args:
            value: float, the translateX value
        """

        self['translateX'] = value

    @property
    def translateY(self) -> float:

        """
        Get the translateY value

        Returns:
            float: the translateY value
        """

        return self['translateY'].asFloat()

    @translateY.setter
    def translateY(self, value: float) -> None:

        """
        Set the translateY value

        Args:
            value: float, the translateY value
        """

        self['translateY'] = value

    @property
    def translateZ(self) -> float:

        """
        Get the translateZ value

        Returns:
            float: the translateZ value
        """

        return self['translateZ'].asFloat()

    @translateZ.setter
    def translateZ(self, value: float) -> None:

        """
        Set the translateZ value

        Args:
            value: float, the translateZ value
        """
        
        self['translateZ'] = value

    @property
    def rotate(self) -> List[float]:

        """
        Get the rotate value

        Returns:
            List[float]: the rotate value
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

        Args:
            value: List[float], the rotate value
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

        Returns:
            List[float]: the rotateX value
        """

        return self['rotateX'].asMAngle().asDegrees()

    @rotateX.setter
    def rotateX(self, value) -> None:
        
        """
        Set the rotate value

        Args:
            value: List[float], the rotate value
        """

        angle = om.MAngle(value).asRadians()

        self['rotateX'] = angle

    @property
    def rotateY(self) -> float:
        
        """
        Get the rotateY value

        Returns:
            List[float]: the rotateY value
        """

        return self['rotateY'].asMAngle().asDegrees()

    @rotateY.setter
    def rotateY(self, value) -> None:
        
        """
        Set the rotateY value

        Args:
            value: List[float], the rotateY value
        """

        self['rotateY'] = om.MAngle(value).asRadians()

    @property
    def rotateZ(self) -> float:
        
        """
        Get the rotateZ value

        Returns:
            List[float]: the rotateZ value
        """

        return self['rotateZ'].asMAngle().asDegrees()

    @rotateZ.setter
    def rotateZ(self, value) -> None:
        
        """
        Set the rotateZ value

        Args:
            value: List[float], the rotateZ value
        """

        self['rotateZ'] = om.MAngle(value).asRadians()

    @property
    def scale(self) -> List[float]:

        """
        Get the scale value

        Returns:
            List[float]: the scale value
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

        Args:
            value: List[float], the scale value
        """

        self['scale'] = value

    @property
    def scaleX(self) -> float:

        """
        Get the scaleX value

        Returns:
            List[float]: the scaleX value
        """

        return self['scaleX'].asFloat()

    @scaleX.setter
    def scaleX(self, value) -> None:

        """
        Set the scaleX value

        Args:
            value: List[float], the scaleX value
        """

        self['scaleX'] = value

    @property
    def scaleY(self) -> float:

        """
        Get the scaleY value

        Returns:
            List[float]: the scaleY value
        """

        return self['scaleY'].asFloat()

    @scaleY.setter
    def scaleY(self, value) -> None:

        """
        Set the scaleY value

        Args:
            value: List[float], the scaleY value
        """

        self['scaleY'] = value

    @property
    def scaleZ(self) -> float:

        """
        Get the scaleZ value

        Returns:
            List[float]: the scale value
        """

        return self['scaleZ'].asFloat()

    @scaleZ.setter
    def scaleZ(self, value) -> None:

        """
        Set the scaleZ value

        Args:
            value: List[float], the scaleZ value
        """

        self['scaleZ'] = value

    @property
    def rotateOrder(self) -> int:
        """
        Get the current transforms rotate order

        Returns:
            int, the chosen rotate order index
        """
        return self['rotateOrder'].asInt()

    @rotateOrder.setter
    def rotateOrder(self, value: Union[int, str]) -> None:
        """
        Set the current transform's rotate order

        Args:
            value: int | str, the rotate order to set, either the index or the
                string (ie: "xyz")
        """
        if isinstance(value, int):
            self['rotateOrder'] = value

        elif isinstance(value, str) and value in self.rotateOrderList:
            self['rotateOrder'] = self.rotateOrderList.index(value)


NodeRegistry()[Transform.nodeType()] = Transform
