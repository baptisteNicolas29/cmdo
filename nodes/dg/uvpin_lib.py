from typing import List, Tuple

from maya import cmds as mc
from maya.api import OpenMaya as om

from ...core.abstract import dg_lib
from ...core.node_registry import NodeRegistry
from ...core.exceptions import CmdoPlugException


class UVPin(dg_lib.DGNode):

    _NODE_TYPE = "uvPin"
    _API_TYPE = om.MFn.kUVPin

    def __init__(self, name: str | om.MObject = None) -> None:

        """
        Initialize an instance of UVPin

        Args:
            name: str | om.MObject, the name of the node
        """

        super().__init__(name=name)

    @property
    def axisList(self) -> List[str]:

        """
        Get the list of available Axis

        Returns:
            List[str]: the list of available axis
        """

        return ['x', 'y', 'z', '-x', '-y', '-z']

    @property
    def normalOverrideList(self) -> List[str]:

        """
        Get the list of available Normal Overrides

        Returns:
            List[str]: the list of available normal overrides
        """

        return ['Auto', 'Rail Curve']

    @property
    def relativeSpaceList(self) -> List[str]:

        """
        Get the list of available Relative Spaces

        Returns:
            List[str]: the list of available relative spaces
        """

        return ['World', 'Local', 'Custom']

    @property
    def coordinateCount(self) -> int:
        """
        Get the number of child coordinate attributes
        from the compound (numElements)

        Returns:
            int: the number of child coordinate attributes from the compound
        """

        return self['coordinate'].numElements()

    @property
    def outputMatrixCount(self) -> int:
        """
        Get the number of child outputMatrix attributes
        from the compound (numElements)

        Returns:
            int: the number of child outputMatrix attributes from the compound
        """

        return self['outputMatrix'].numElements()

    @property
    def deformedGeometry(self) -> om.MObject | None:

        """
        Get the deformedGeometry source plug

        Returns:
             om.MObject | None: the deformedGeometry source plug or None
        """

        deformedGeometry = self['deformedGeometry']
        if deformedGeometry.source().isNull:
            return None

        return deformedGeometry.source().name()

    @deformedGeometry.setter
    def deformedGeometry(self, value: om.MPlug) -> None:

        """
        Set the deformedGeometry source plug

        Args:
             value: om.MPlug, the deformedGeometry source plug
        """

        self['deformedGeometry'] = value

    @property
    def originalGeometry(self) -> om.MObject | None:

        """
        Get the originalGeometry source plug

        Returns:
             om.MObject | None: the originalGeometry source plug or None
        """

        originalGeometry = self['originalGeometry']
        if originalGeometry.source().isNull:
            return None

        return originalGeometry.source().name()

    @originalGeometry.setter
    def originalGeometry(self, value: om.MPlug) -> None:

        """
        Set the originalGeometry source plug

        Args:
             value: om.MPlug, the originalGeometry source plug
        """

        self['originalGeometry'] = value
    
    @property
    def normalAxis(self) -> int:

        """
        Get the normalAxis value

        Returns:
            int: the normalAxis value
        """

        return self['normalAxis'].asInt()

    @normalAxis.setter
    def normalAxis(self, value: int | str) -> None:

        """
        Set the normalAxis value

        Args:
            value: int | str, the normal axis to set, either the index or the
                string (ie: "y")
        """

        if isinstance(value, int):
            self['normalAxis'] = value

        elif isinstance(value, str) and value in self.axisList:
            self['normalAxis'] = self.axisList.index(value)

        else:
            raise CmdoPlugException(
                f'{self.name}: NormalAxis needs valid input, got {value}'
            )

    @property
    def tangentAxis(self) -> int:

        """
        Get the tangentAxis value

        Returns:
            int: the tangentAxis value
        """

        return self['tangentAxis'].asInt()

    @tangentAxis.setter
    def tangentAxis(self, value: int | str) -> None:

        """
        Set the tangentAxis value

        Args:
            value: int | str, the normal axis to set, either the index or the
                string (ie: "-y")
        """

        if isinstance(value, int):
            self['tangentAxis'] = value

        elif isinstance(value, str) and value in self.axisList:
            self['tangentAxis'] = self.axisList.index(value)

        else:
            raise CmdoPlugException(
                f'{self.name}: tangentAxis needs valid input, got {value}'
            )

    @property
    def uvSetName(self) -> str:

        """
        Get the uvSetName value

        Returns:
            str: the uvSetName value
        """

        return self['uvSetName'].asString()

    @uvSetName.setter
    def uvSetName(self, value: str) -> None:

        """
        Set the uvSetName value

        Args:
            value: str, the uvSetName value
        """

        self['uvSetName'] = value

    @property
    def normalizedIsoparms(self) -> bool:

        """
        Get the normalizedIsoparms value

        Returns:
            bool: the normalizedIsoparms value
        """

        return self['normalizedIsoparms'].asBool()

    @normalizedIsoparms.setter
    def normalizedIsoparms(self, value: bool) -> None:

        """
        Set the normalizedIsoparms value

        Args:
            value: bool, the normalizedIsoparms value
        """

        self['normalizedIsoparms'] = value

    @property
    def normalOverride(self) -> int:

        """
        Get the normalOverride value

        Returns:
            int: the normalOverride value
        """

        return self['normalOverride'].asInt()

    @normalOverride.setter
    def normalOverride(self, value: int | str) -> None:

        """
        Set the normalOverride value

        Args:
            value: int | str, the normal override to set, either the index or
                the string (ie: "Auto")
        """

        if isinstance(value, int):
            self['normalOverride'] = value

        elif isinstance(value, str) and value in self.normalOverrideList:
            self['normalOverride'] = self.normalOverrideList.index(value)

        else:
            raise CmdoPlugException(
                f'{self.name}: normalOverride needs valid input, got {value}'
            )

    @property
    def relativeSpaceMode(self) -> int:

        """
        Get the relativeSpaceMode value

        Returns:
            int: the relativeSpaceMode value
        """

        return self['relativeSpaceMode'].asInt()

    @relativeSpaceMode.setter
    def relativeSpaceMode(self, value: int | str) -> None:

        """
        Set the relativeSpaceMode value

        Args:
            value: int | str, the relative space to set, either the index or
                the string (ie: "World")
        """

        if isinstance(value, int):
            self['relativeSpaceMode'] = value

        elif isinstance(value, str) and value in self.relativeSpaceList:
            self['relativeSpaceMode'] = self.relativeSpaceList.index(value)

        else:
            raise CmdoPlugException(
                f'{self.name}: relativeSpaceMode needs valid input, got {value}'
            )

    @property
    def relativeSpaceMatrix(self) -> List[float]:
        """
        Get the relativeSpaceMatrix value

        Returns:
            List[float]: the relativeSpaceMatrix value
        """

        return self['relativeSpaceMatrix'].value

    @relativeSpaceMatrix.setter
    def relativeSpaceMatrix(self, value: om.MPlug | List[float]) -> None:

        """
        Set the relativeSpaceMatrix value

        Args:
            value: bool, the relativeSpaceMatrix value
        """

        self['relativeSpaceMatrix'] = value

    def getCoordinate(self, index: int) -> Tuple[float, float]:
        """
        Get the coordinate from a target index value

        Args:
            index: int, the index of the coordinate to get

        Returns:
            Tuple[float, float]: the coordinate value
        """

        return self['coordinate'][index].value

    def setCoordinate(self, index: int, value: Tuple[float, float] | om.MPlug) -> None:
        """
        Set the coordinate from a target index value

        Args:
            index: int, the index of the coordinate to get
            value: Tuple[float, float], the coordinate value
        """

        self['coordinate'][index] = value

    def getCoordinateU(self, index: int) -> Tuple[float, float]:
        """
        Get the coordinateU from a target index value

        Args:
            index: int, the index of the coordinateU to get

        Returns:
            Tuple[float, float]: the coordinateU value
        """

        return self['coordinate'][index]['coordinateU'].asFloat()

    def setCoordinateU(self, index: int, value: Tuple[float, float] | om.MPlug) -> None:
        """
        Set the coordinateU from a target index value

        Args:
            index: int, the index of the coordinateU to get
            value: Tuple[float, float], the coordinateU value
        """

        self['coordinate'][index]['coordinateU'] = value
        
    def getCoordinateV(self, index: int) -> Tuple[float, float]:
        """
        Get the coordinateV from a target index value

        Args:
            index: int, the index of the coordinateV to get

        Returns:
            Tuple[float, float]: the coordinateV value
        """

        return self['coordinate'][index]['coordinateV'].asFloat()

    def setCoordinateV(self, index: int, value: Tuple[float, float] | om.MPlug) -> None:
        """
        Set the coordinateV from a target index value

        Args:
            index: int, the index of the coordinateV to get
            value: Tuple[float, float], the coordinateV value
        """

        self['coordinate'][index]['coordinateV'] = value
    
    def getOutputMatrix(self, index: int) -> List[float]:
        """
        Get the outputMatrix from a target index value

        Args:
            index: int, the index of the outputMatrix to get

        Returns:
            List[float]: the outputMatrix value
        """

        return self['outputMatrix'][index].value


NodeRegistry()[UVPin.nodeType()] = UVPin
