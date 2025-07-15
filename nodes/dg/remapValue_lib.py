from typing import Optional, List, Union

from maya.api import OpenMaya as om

from ...core import convert
from ...core.abstract import dg_lib
from ...core.node_registry import NodeRegistry


class RemapValue(dg_lib.DGNode):

    _NODE_TYPE = "remapValue"
    _API_TYPE = om.MFn.kRemapValue

    def __init__(self, name: str | om.MObject = None) -> None:
        """
        Initialize an instance of RemapValue

        Args:
            name: str | om.MObject, the name of the node
        """

        super().__init__(name=name)

    @property
    def inputMin(self) -> float:
        """
        Get the inputMin value

        Returns:
            float, the inputMin value
        """

        return self['inputMin'].asFloat()

    @inputMin.setter
    def inputMin(self, value: float) -> None:
        """
        Set the inputMin value

        Args:
            value: float, the inputMin value
        """

        self['inputMin'] = value

    @property
    def inputMax(self) -> float:
        """
        Get the inputMax value

        Returns:
            float, the inputMax value
        """

        return self['inputMax'].asFloat()

    @inputMax.setter
    def inputMax(self, value: float) -> None:
        """
        Set the inputMax value

        Args:
            value: float, the inputMax value
        """

        self['inputMax'] = value

    @property
    def inputValue(self) -> float:
        """
        Get the inputValue value

        Returns:
            float, the inputValue value
        """

        return self['inputValue'].asFloat()

    @inputValue.setter
    def inputValue(self, value: float) -> None:
        """
        Set the inputValue value

        Args:
            value: float, the inputValue value
        """

        self['inputValue'] = value

    @property
    def outputMin(self) -> float:
        """
        Get the outputMin value

        Returns:
            float, the outputMin value
        """

        return self['outputMin'].asFloat()
    
    @outputMin.setter
    def outputMin(self, value: float) -> None:
        """
        Set the outputMin value

        Args:
            value: float, the outputMin value
        """

        self['outputMin'] = value

    @property
    def outputMax(self) -> float:
        """
        Get the outputMax value

        Returns:
            float, the outputMax value
        """

        return self['outputMax'].asFloat()
    
    @outputMax.setter
    def outputMax(self, value: float) -> None:
        """
        Set the outputMax value

        Args:
            value: float, the outputMax value
        """

        self['outputMax'] = value

    @property
    def colorCount(self) -> int:
        """
        Get the number of color compound attributes (numElements)

        Returns:
            int: the number of color compound attributes
        """

        return self['color'].numElements()

    @property
    def valueCount(self) -> int:
        """
        Get the number of value compound attributes (numElements)

        Returns:
            int: the number of value compound attributes
        """

        return self['value'].numElements()

    def getColorPosition(self, index: int) -> float:
        """
        Get the color[index].color_Position value

        Args:
            index: int, the index of the color value to get

        Returns:
            float, the color[index].color_Position value
        """

        return self['color'][index]['color_Position'].asFloat()

    def setColorPosition(self, index: int, value: float) -> None:
        """
        Set the color[index].color_Position value

        Args:
            index: int, the index of the color value to get
            value: float, the color[index].color_Position value
        """

        self['color'][index]['color_Position'] = value

    def getColorInterp(self, index: int) -> float:
        """
        Get the color[index].color_Interp value

        Args:
            index: int, the index of the color value to get

        Returns:
            float, the color[index].color_Interp value
        """

        return self['color'][index]['color_Interp'].asFloat()

    def setColorInterp(self, index: int, value: float) -> None:
        """
        Set the color[index].color_Interp value

        Args:
            index: int, the index of the color value to get
            value: float, the color[index].color_Interp value
        """

        self['color'][index]['color_Interp'] = value
        
    def getColorColor(self, index: int) -> List[float]:
        """
        Get the color[index].color_Color value

        Args:
            index: int, the index of the color value to get

        Returns:
            List[float], the color[index].color_Color value
        """

        return self['color'][index]['color_Color'].asFloat()

    def setColorColor(self, index: int, value: List[float]) -> None:
        """
        Set the color[index].color_Color value

        Args:
            index: int, the index of the color value to get
            value: List[float], the color[index].color_Color value
        """

        self['color'][index]['color_Color'] = value
        
    def getColorColorR(self, index: int) -> float:
        """
        Get the color[index].color_ColorR value

        Args:
            index: int, the index of the color value to get

        Returns:
            float, the color[index].color_ColorR value
        """

        return self['color'][index]['color_ColorR'].asFloat()

    def setColorColorR(self, index: int, value: float) -> None:
        """
        Set the color[index].color_ColorR value

        Args:
            index: int, the index of the color value to get
            value: float, the color[index].color_ColorR value
        """

        self['color'][index]['color_ColorR'] = value

    def getColorColorG(self, index: int) -> float:
        """
        Get the color[index].color_ColorG value

        Args:
            index: int, the index of the color value to get

        Returns:
            float, the color[index].color_ColorG value
        """

        return self['color'][index]['color_ColorG'].asFloat()

    def setColorColorG(self, index: int, value: float) -> None:
        """
        Set the color[index].color_ColorG value

        Args:
            index: int, the index of the color value to get
            value: float, the color[index].color_ColorG value
        """

        self['color'][index]['color_ColorG'] = value

    def getColorColorB(self, index: int) -> float:
        """
        Get the color[index].color_ColorB value

        Args:
            index: int, the index of the color value to get

        Returns:
            float, the color[index].color_ColorB value
        """

        return self['color'][index]['color_ColorB'].asFloat()

    def setColorColorB(self, index: int, value: float) -> None:
        """
        Set the color[index].color_ColorB value

        Args:
            index: int, the index of the color value to get
            value: float, the color[index].color_ColorB value
        """

        self['color'][index]['color_ColorB'] = value

    def getValuePosition(self, index: int) -> float:
        """
        Get the value[index].value_Position value

        Args:
            index: int, the index of the value Position to get

        Returns:
            float, the value[index].value_Position value
        """

        return self['value'][index]['value_Position'].asFloat()

    def setValuePosition(self, index: int, value: float) -> None:
        """
        Set the value[index].value_Position value

        Args:
            index: int, the index of the value Position to get
            value: float, the value[index].value_Position value
        """

        self['value'][index]['value_Position'] = value

    def getValueInterp(self, index: int) -> int:
        """
        Get the value[index].value_Interp value

        Args:
            index: int, the index of the value Interp to get

        Returns:
            int, the value[index].value_Interp value
        """

        return self['value'][index]['value_Interp'].asInt()

    def setValueInterp(self, index: int, value: int) -> None:
        """
        Set the value[index].value_Interp value

        Args:
            index: int, the index of the value Interp to get
            value: int, the value[index].value_Interp value
        """

        self['value'][index]['value_Interp'] = value

    def getValueFloatValue(self, index: int) -> float:
        """
        Get the value[index].value_FloatValue value

        Args:
            index: int, the index of the value FloatValue to get

        Returns:
            float, the value[index].value_FloatValue value
        """

        return self['value'][index]['value_FloatValue'].asFloat()

    def setValueFloatValue(self, index: int, value: float) -> None:
        """
        Set the value[index].value_FloatValue value

        Args:
            index: int, the index of the value FloatValue to get
            value: float, the value[index].value_FloatValue value
        """

        self['value'][index]['value_FloatValue'] = value


NodeRegistry()[RemapValue.nodeType()] = RemapValue
