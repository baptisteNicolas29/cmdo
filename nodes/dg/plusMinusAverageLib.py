from typing import List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


# Attribute names in this node are inconsistent with other nodes
# Instead of output3DX, this node has output3Dx (upper -> lower case "X")
# We implement as it is designed inside of Maya

# TODO: ALSO, since input2D and input3D are compoundAttributes
#  containing multiAttributes, to set one of them ie: input2D[index],
#  we need to give as argument an iterable of an iterable
#  ie: pm.setInput2D(index, [[1, 2]])
#  this will set the x and y component of the input2D[index] where x=1 and y=2
#  otherwise we can set specific components of the multiAttribute one by one
#  ie: pm.setInput2Dx(index, 1)
#  ie: pm.setInput2Dy(index, 2)
#  THIS IS ANNOYING WE NEED TO FIX THIS!!!!!

class PlusMinusAverage(dgLib.DGNode):

    _NODE_TYPE = "plusMinusAverage"
    _API_TYPE = om.MFn.kPlusMinusAverage

    def __init__(self, name: Union[str, om.MObject] = None) -> None:
        """
        Initialize an instance of PlusMinusAverage

        Args:
            name: str | om.MObject, the name of the node
        """

        super().__init__(name=name)

    @property
    def operationList(self) -> List[str]:

        """
        Get the list of available operations

        Returns:
            List[str]: the list of available operations
        """

        return ['No Operation', 'Sum', 'Subtract', 'Average']

    @property
    def operation(self) -> int:
        """
        Get the operation value

        Returns:
            int: the operation value
        """

        return self['operation'].asInt()

    @operation.setter
    def operation(self, value: Union[int, str]):

        """
        Set the operation value

        Args:
            value: int | str, the operation to set, either the index or the
                string (ie: "xyz")
        """

        if isinstance(value, int) and 0 < value < len(self.operationList):
            self['operation'] = value

        elif isinstance(value, str) and value in self.operationList:
            self['operation'] = self.operationList.index(value)

        else:
            err_str = [f'{i} - {s}' for i, s in enumerate(self.operationList)]
            raise AttributeError(
                f'{self.name}: Operation needs valid input, got {value}'
                f'\nNeeded int or string: {err_str}'
            )

    @property
    def input1DCount(self) -> int:
        """
        Get the number of input1D compound attributes (numElements)

        Returns:
            int: the number of input1D compound attributes
        """

        return self['input1D'].numElements()

    @property
    def input2DCount(self) -> int:
        """
        Get the number of input2D compound attributes (numElements)

        Returns:
            int: the number of input2D compound attributes
        """

        return self['input2D'].numElements()

    @property
    def input3DCount(self) -> int:
        """
        Get the number of input3D compound attributes (numElements)

        Returns:
            int: the number of input3D compound attributes
        """

        return self['input3D'].numElements()

    def getInput1D(self, index: int) -> List[float]:
        """
        Get the input1D from a target index value

        Args:
            index: int, the index of the input1D to get value from

        Returns:
            List[float]: the input1D value
        """

        return self['input1D'][index].asFloat()

    def setInput1D(self, index: int, value: Union[float, om.MPlug]) -> None:
        """
        Set the input1D from a target index value

        Args:
            index: int, the index of the input1D to get value from
            value: List[float], the input1D value
        """

        self['input1D'][index] = value

    def getInput2D(self, index: int) -> List[float]:
        """
        Get the input2D from a target index value

        Args:
            index: int, the index of the input2D to get value from

        Returns:
            List[float]: the input2D value
        """

        return self['input2D'][index].value

    def setInput2D(self, index: int, value: Union[List[float], om.MPlug]) -> None:
        """
        Set the input2D from a target index value

        Args:
            index: int, the index of the input2D to get value from
            value: List[float], the input2D value
        """

        self['input2D'][index] = value
        
    def getInput2Dx(self, index: int) -> float:
        """
        Get the input2Dx from a target index value

        Args:
            index: int, the index of the input2Dx to get value from

        Returns:
            List[float]: the input2Dx value
        """

        return self['input2D'][index]['input2Dx'].asFloat()

    def setInput2Dx(self, index: int, value: Union[float, om.MPlug]) -> None:
        """
        Set the input2Dx from a target index value

        Args:
            index: int, the index of the input2Dx to get value from
            value: List[float], the input2Dx value
        """

        self['input2D'][index]['input2Dx'] = value
        
    def getInput2Dy(self, index: int) -> float:
        """
        Get the input2Dy from a target index value

        Args:
            index: int, the index of the input2Dy to get value from

        Returns:
            List[float]: the input2Dy value
        """

        return self['input2D'][index]['input2Dy'].asFloat()

    def setInput2Dy(self, index: int, value: Union[float, om.MPlug]) -> None:
        """
        Set the input2Dy from a target index value

        Args:
            index: int, the index of the input2Dy to get value from
            value: List[float], the input2Dy value
        """

        self['input2D'][index]['input2Dy'] = value

    def getInput3D(self, index: int) -> List[float]:
        """
        Get the input3D from a target index value

        Args:
            index: int, the index of the input3D to get value from

        Returns:
            List[float]: the input3D value
        """

        return self['input3D'][index].value

    def setInput3D(self, index: int, value: Union[List[float], om.MPlug]) -> None:
        """
        Set the input3D from a target index value

        Args:
            index: int, the index of the input3D to get value from
            value: List[float], the input3D value
        """

        self['input3D'][index] = value

    def getInput3Dx(self, index: int) -> float:
        """
        Get the input3Dx from a target index value

        Args:
            index: int, the index of the input3Dx to get value from

        Returns:
            List[float]: the input3Dx value
        """

        return self['input3D'][index]['input3Dx'].asFloat()

    def setInput3Dx(self, index: int, value: Union[float, om.MPlug]) -> None:
        """
        Set the input3Dx from a target index value

        Args:
            index: int, the index of the input3Dx to get value from
            value: List[float], the input3Dx value
        """

        self['input3D'][index]['input3Dx'] = value

    def getInput3Dy(self, index: int) -> float:
        """
        Get the input3Dy from a target index value

        Args:
            index: int, the index of the input3Dy to get value from

        Returns:
            List[float]: the input3Dy value
        """

        return self['input3D'][index]['input3Dy'].asFloat()

    def setInput3Dy(self, index: int, value: Union[float, om.MPlug]) -> None:
        """
        Set the input3Dy from a target index value

        Args:
            index: int, the index of the input3Dy to get value from
            value: List[float], the input3Dy value
        """

        self['input3D'][index]['input3Dy'] = value
        
    def getInput3Dz(self, index: int) -> float:
        """
        Get the input3Dz from a target index value

        Args:
            index: int, the index of the input3Dz to get value from

        Returns:
            List[float]: the input3Dz value
        """

        return self['input3D'][index]['input3Dz'].asFloat()

    def setInput3Dz(self, index: int, value: Union[float, om.MPlug]) -> None:
        """
        Set the input3Dz from a target index value

        Args:
            index: int, the index of the input3Dz to get value from
            value: List[float], the input3Dz value
        """

        self['input3D'][index]['input3Dz'] = value

    @property
    def output1D(self) -> float:
        """
        Get the output1D value

        Returns:
            float: the output1D value
        """

        return self['output1D'].asFloat()

    @property
    def output2D(self) -> List[float]:
        """
        Get the output2D value

        Returns:
            List[float]: the output2D value
        """

        return [
            self.output2Dx,
            self.output2Dy
        ]

    @property
    def output2Dx(self) -> float:
        """
        Get the output2DX value

        Returns:
            float: the output2DX value
        """

        return self['output2Dx'].asFloat()

    @property
    def output2Dy(self) -> float:
        """
        Get the output2DY value

        Returns:
            float: the output2DY value
        """

        return self['output2Dy'].asFloat()

    @property
    def output3D(self) -> List[float]:
        """
        Get the output3D value

        Returns:
            List[float]: the output3D value
        """

        return [
            self.output3Dx,
            self.output3Dy,
            self.output3Dz
        ]

    @property
    def output3Dx(self) -> float:
        """
        Get the output3DX value

        Returns:
            List[float]: the output3DX value
        """

        return self['output3Dx'].asFloat()

    @property
    def output3Dy(self) -> float:
        """
        Get the output3DY value

        Returns:
            List[float]: the output3DY value
        """

        return self['output3Dy'].asFloat()

    @property
    def output3Dz(self) -> float:
        """
        Get the output3DZ value

        Returns:
            List[float]: the output3DZ value
        """

        return self['output3Dz'].asFloat()


NodeRegistry()[PlusMinusAverage.nodeType()] = PlusMinusAverage
