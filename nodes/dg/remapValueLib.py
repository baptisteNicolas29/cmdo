from typing import Optional, List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class RemapValue(dgLib.DGNode):

    _NODE_TYPE = "remapValue"
    _API_TYPE = om.MFn.kRemapValue

    @property
    def inputMin(self) -> float:
        """
        Get the inputMin value

        :return: float, the inputMin value
        """

        return self['inputMin'].asFloat()

    @inputMin.setter
    def inputMin(self, value: float) -> None:
        """
        Set the inputMin value

        :param value: float, the inputMin value
        """

        self['inputMin'] = value

    @property
    def inputMax(self) -> float:
        """
        Get the inputMax value

        :return: float, the inputMax value
        """

        return self['inputMax'].asFloat()

    @inputMax.setter
    def inputMax(self, value: float) -> None:
        """
        Set the inputMax value

        :param value: float, the inputMax value
        """

        self['inputMax'] = value

    @property
    def inputValue(self) -> float:
        """
        Get the inputValue value

        :return: float, the inputValue value
        """

        return self['inputValue'].asFloat()

    @inputValue.setter
    def inputValue(self, value: float) -> None:
        """
        Set the inputValue value

        :param value: float, the inputValue value
        """

        self['inputValue'] = value

    @property
    def outputMin(self) -> float:
        """
        Get the outputMin value

        :return: float, the outputMin value
        """

        return self['outputMin'].asFloat()
    
    @outputMin.setter
    def outputMin(self, value: float) -> None:
        """
        Set the outputMin value

        :param value: float, the outputMin value
        """

        self['outputMin'] = value

    @property
    def outputMax(self) -> float:
        """
        Get the outputMax value

        :return: float, the outputMax value
        """

        return self['outputMax'].asFloat()
    
    @outputMax.setter
    def outputMax(self, value: float) -> None:
        """
        Set the outputMax value

        :param value: float, the outputMax value
        """

        self['outputMax'] = value

    @property
    def colorCount(self) -> int:
        """
        Get the number of color compound attributes (numElements)

        :return: int, the number of color compound attributes
        """

        return self['color'].numElements()

    @property
    def valueCount(self) -> int:
        """
        Get the number of value compound attributes (numElements)

        :return: int, the number of value compound attributes
        """

        return self['value'].numElements()

    def getColorPosition(self, index: int) -> float:
        """
        Get the color[index].color_Position value

        :param index: int, the index of the color value to get

        :return: float, the color[index].color_Position value
        """

        return self['color'][index]['color_Position'].asFloat()

    def setColorPosition(self, index: int, value: float) -> None:
        """
        Set the color[index].color_Position value

        :param index: int, the index of the color value to get
        :param value: float, the color[index].color_Position value
        """

        self['color'][index]['color_Position'] = value

    def getColorInterp(self, index: int) -> float:
        """
        Get the color[index].color_Interp value

        :param index: int, the index of the color value to get

        :return: float, the color[index].color_Interp value
        """

        return self['color'][index]['color_Interp'].asFloat()

    def setColorInterp(self, index: int, value: float) -> None:
        """
        Set the color[index].color_Interp value

        :param index: int, the index of the color value to get
        :param value: float, the color[index].color_Interp value
        """

        self['color'][index]['color_Interp'] = value
        
    def getColorColor(self, index: int) -> List[float]:
        """
        Get the color[index].color_Color value

        :param index: int, the index of the color value to get

        :return: List[float], the color[index].color_Color value
        """

        return self['color'][index]['color_Color'].asFloat()

    def setColorColor(self, index: int, value: List[float]) -> None:
        """
        Set the color[index].color_Color value

        :param index: int, the index of the color value to get
        :param value: List[float], the color[index].color_Color value
        """

        self['color'][index]['color_Color'] = value
        
    def getColorColorR(self, index: int) -> float:
        """
        Get the color[index].color_ColorR value

        :param index: int, the index of the color value to get

        :return: float, the color[index].color_ColorR value
        """

        return self['color'][index]['color_ColorR'].asFloat()

    def setColorColorR(self, index: int, value: float) -> None:
        """
        Set the color[index].color_ColorR value

        :param index: int, the index of the color value to get
        :param value: float, the color[index].color_ColorR value
        """

        self['color'][index]['color_ColorR'] = value

    def getColorColorG(self, index: int) -> float:
        """
        Get the color[index].color_ColorG value

        :param index: int, the index of the color value to get

        :return: float, the color[index].color_ColorG value
        """

        return self['color'][index]['color_ColorG'].asFloat()

    def setColorColorG(self, index: int, value: float) -> None:
        """
        Set the color[index].color_ColorG value

        :param index: int, the index of the color value to get
        :param value: float, the color[index].color_ColorG value
        """

        self['color'][index]['color_ColorG'] = value

    def getColorColorB(self, index: int) -> float:
        """
        Get the color[index].color_ColorB value

        :param index: int, the index of the color value to get

        :return: float, the color[index].color_ColorB value
        """

        return self['color'][index]['color_ColorB'].asFloat()

    def setColorColorB(self, index: int, value: float) -> None:
        """
        Set the color[index].color_ColorB value

        :param index: int, the index of the color value to get
        :param value: float, the color[index].color_ColorB value
        """

        self['color'][index]['color_ColorB'] = value

    def getValuePosition(self, index: int) -> float:
        """
        Get the value[index].value_Position value

        :param index: int, the index of the value Position to get

        :return: float, the value[index].value_Position value
        """

        return self['value'][index]['value_Position'].asFloat()

    def setValuePosition(self, index: int, value: float) -> None:
        """
        Set the value[index].value_Position value

        :param index: int, the index of the value Position to get
        :param value: float, the value[index].value_Position value
        """

        self['value'][index]['value_Position'] = value

    def getValueInterp(self, index: int) -> int:
        """
        Get the value[index].value_Interp value

        :param index: int, the index of the value Interp to get

        :return: int, the value[index].value_Interp value
        """

        return self['value'][index]['value_Interp'].asInt()

    def setValueInterp(self, index: int, value: int) -> None:
        """
        Set the value[index].value_Interp value

        :param index: int, the index of the value Interp to get
        :param value: int, the value[index].value_Interp value
        """

        self['value'][index]['value_Interp'] = value

    def getValueFloatValue(self, index: int) -> float:
        """
        Get the value[index].value_FloatValue value

        :param index: int, the index of the value FloatValue to get

        :return: float, the value[index].value_FloatValue value
        """

        return self['value'][index]['value_FloatValue'].asFloat()

    def setValueFloatValue(self, index: int, value: float) -> None:
        """
        Set the value[index].value_FloatValue value

        :param index: int, the index of the value FloatValue to get
        :param value: float, the value[index].value_FloatValue value
        """

        self['value'][index]['value_FloatValue'] = value


NodeRegistry()[RemapValue.nodeType()] = RemapValue
