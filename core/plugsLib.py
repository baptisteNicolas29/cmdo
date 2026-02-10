from typing import Union, Any, Type, Tuple

import math

from maya import cmds
from maya.api import OpenMaya as om

from .exceptions import CmdoPlugException


class Plug(om.MPlug):
    _DEFAULT = object()

    def __init__(self, *args: Union[str, Tuple[om.MObject, om.MObject], 'Plug']) -> None:
        """
        Initialize an instance of Plug

        :param args: Union[str, Tuple[om.MObject, om.MObject], 'Plug'],
            Plug can be initialised with a str (nodeName.plugName),
            two MObjects (node, attribute) or a Plug (Plug/MPlug object)
        """

        if isinstance(args[0], str):
            selList = om.MSelectionList()
            args = [selList.add(args).getPlug(0)]

        super().__init__(*args)

    def __hash__(self) -> int:
        """
        Make hash using long name and uuid to try having a unique hash

        We "cache" the hash to avoid it changing in the middle of maya operation
        """

        if hasattr(self, '_HASH'):
            return self._HASH

        self._HASH = self.node().hash + hash(self.name())
        return self._HASH

    def __iter__(self, *args, **kwargs) -> om.MPlug:

        if self.isNull:
            return

        if self.multi:
            for index in range(self.numElements()):
                result = self.__class__(self.elementByPhysicalIndex(index))
                yield result

        elif self.isCompound:
            for index in range(self.numChildren()):
                result = self.__class__(self.child(index))
                yield result

        else:
            raise TypeError(f"{self} is not an iterable plug")

    def __getitem__(self, value: Union[int, str]) -> 'Plug':
        """
        __getitem__ implementation
            - plug["childPlug"]
            - plug[1]

        :param value: Union[int, str], name or index of the child or multi attribute

        :return: om.MPlug, retrieve the plug
        """

        # implement str input (for child version)
        if isinstance(value, str):
            for idx in range(self.numChildren()):

                child = self.child(idx)
                afn = om.MFnAttribute(child.attribute())
                aliasName = child.partialName(includeNodeName=False, useAlias=True)

                if value in [afn.name, afn.shortName, aliasName]:
                    return self.__class__(child)

        # implement int input can be array if attribute
        # is array else try to compute child plug
        elif isinstance(value, int):
            if self.multi:
                return self.__class__(self.elementByLogicalIndex(value))

            elif self.isCompound:
                return self.__class__(self.child(value))

        elif isinstance(value, slice):
            plugs = []

            if self.multi:

                byLogical = False
                if self.numElements() == 0 and (value.stop is None):
                    raise CmdoPlugException(f"{self} is a zero size array, stop slice needed")

                start, stop, step = value.indices(self.numElements())
                if not self.numElements():
                    byLogical = True

                    if value.stop <= 0:
                        raise CmdoPlugException(f"{self} has zero lenght no negative stop")
                    stop = value.stop

                for index in range(start, stop, step):
                    plug = None
                    if byLogical:

                        plug = self.__class__(self.elementByLogicalIndex(index))
                        plugs.append(plug)

                    else:
                        plugs.append(self.__class__(self.elementByPhysicalIndex(index)))

            elif self.isCompound:
                if value.stop:
                    if not -self.numChildren() - 1 < value.stop < self.numChildren():
                        raise IndexError(f"stop value: {value.stop} out of range {self} size")

                start, stop, step = value.indices(self.numChildren())

                for index in range(start, stop, step):
                    plugs.append(self.__class__(self.child(index)))

            return plugs

        else:
            raise KeyError(f"plug getItem need str or int got {type(value)}")

        raise AttributeError(f'{self} does not have attribute {value}')

    def __setitem__(self, key: str, value: Any) -> None:

        # TODO: need to fix this part with the * operator, some types of
        #  attributes don t play well with this implementation

        if isinstance(value, (tuple, list)):
            self[key].set(*value)

        else:
            self[key].set(value)

    def __str__(self) -> str:

        if self.isNull:
            return ''

        selList = om.MSelectionList()
        selList.add(self)

        return selList.getSelectionStrings()[0]

    def __repr__(self) -> str:

        if self.isNull:
            return f'{self.__class__.__name__}()'

        return f"{self.__class__.__name__}({repr(self.name())})"

    def __iadd__(self, other: Any):

        if isinstance(other, self.__class__):
            other = other.value

        self.value = self.value + other

        return self.value

    def __isub__(self, other: Any):

        if isinstance(other, self.__class__):
            other = other.value

        self.value = self.value - other
        return self.value

    def __imul__(self, other: Any):

        if isinstance(other, self.__class__):
            other = other.value

        self.value = self.value * other
        return self.value

    def __add__(self, other):

        if isinstance(other, self.__class__):
            other = other.value

        return self.value + other

    def __sub__(self, other):

        if isinstance(other, self.__class__):
            other = other.value
        return self.value - other

    def __mul__(self, other):

        if isinstance(other, self.__class__):
            other = other.value

        return self.value * other

    def __rshift__(self, other: 'Plug') -> None:
        self.connect(other)

    def __lshift__(self, other: 'Plug') -> None:
        other.connect(self)

    def __truediv__(self, other: om.MPlug) -> None:
        """
        Implement "/" symbol for disconnecting plugs
        Works in either direction: plug1 / plug2 OR plug2 / plug1

        :param other: om.MPlug, a plug to disconnect
        """

        if not isinstance(other, self.__class__):
            other = Plug(other)

        if other.source() == self:
            self.disconnect(other)

        elif self.source() == other:
            other.disconnect(self)

    def get(self, key: Union[int, str], default=_DEFAULT) -> 'Plug':
        # TODO: implement key on this method like python will do it
        """
        Get the wanted plug from its name plug.get("childPlug")

        :param keyname: Union[int, str], index or name of the asked plug

        :return: om.MPlug, found plug or null plug if not found

        """

        # handle case where source is a null Node
        if self.isNull:
            return self.__class__() if default is self._DEFAULT else default

        try:
            return self[key]

        except:
            if default is self._DEFAULT:
                return self.__class__()

            return default

    def set(self, *value: Any) -> None:

        # TODO: how to check if it is connected but still animatable?
        if self.isLocked:  # or self.isDestination:
            raise CmdoPlugException(
                f'{self.name()} is locked or connected and cannot be set'
            )

        if isinstance(value[0], om.MPlug):
            self.__class__(value[0]).connect(self)

        elif self.isCompound or self.isArray:
            for idx, val in enumerate(*value):

                if self.isCompound:
                    self.child(idx).set(val)

                if self.isArray:
                    self.elementByLogicalIndex(idx).set(val)

        elif self.type == 'doubleAngle':
            radians = math.radians(value[0])
            self.setDouble(radians)

        elif isinstance(value[0], int):
            self.setInt(value[0])

        elif isinstance(value[0], float):
            self.setDouble(value[0])

        elif isinstance(value[0], bool):
            self.setBool(value[0])

        elif isinstance(value[0], str):
            self.setString(value[0])

        elif self.type == 'matrix':
            try:
                if len(value[0]) == 16:
                    value = om.MMatrix(value[0])

                elif isinstance(value[0], om.MMatrix):
                    value = value[0]

                matrixData = om.MFnMatrixData()
                matObj = matrixData.create(value)
                self.setMObject(matObj)

            except Exception:
                raise AttributeError(
                    f'{self.name()}, Wrong input type to set matrix attribute. '
                    f'Got:'
                    f'\n\t- type: {repr(value)} '
                    f'\n\t- len: {len(value)} '
                    f'\n\t- value: {value}'
                )

    def parent(self, *args, **kwargs):
        return self.__class__(super().parent(*args, **kwargs))

    def elementByLogicalIndex(self, *args, **kwargs):
        return self.__class__(super().elementByLogicalIndex(*args, **kwargs))

    def elementByPhysicalIndex(self, *args, **kwargs):
        return self.__class__(super().elementByPhysicalIndex(*args, **kwargs))

    def node(self, *args, **kwargs):
        from .nodeRegistry import NodeRegistry

        mObject = super().node()

        return NodeRegistry().get(mObject)(mObject)

    def child(self, *args, **kwargs) -> 'Plug':
        """
        Get the child plug from given arguments

        :return: Plug, the child plug
        """

        return self.__class__(super().child(*args, **kwargs))

    def source(self, *args, **kwargs) -> 'Plug':
        """
        Get the source of the plug

        :return: Plug, source of the plug

        """

        return self.__class__(super().source())

    def destinations(self, *args, **kwargs) -> 'PlugArray':
        """
         Get the destinations of the plug

        :return: PlugArray, an array of destination plugs

        """

        return PlugArray(super().destinations())

    def connect(self, other: "Plug", force=False) -> None:

        if not isinstance(other, self.__class__):
            return

        if other.isDestination:
            if force:
                dg_modifier = om.MDGModifier()
                dg_modifier.disconnect(other.source(), other)
                dg_modifier.doIt()

            else:
                return

        dg_modifier = om.MDGModifier()
        dg_modifier.connect(self, other)
        dg_modifier.doIt()

    def disconnect(self, other) -> None:

        if not isinstance(other, self.__class__):
            return

        dg_modifier = om.MDGModifier()
        dg_modifier.disconnect(self, other)
        dg_modifier.doIt()

    @property
    def hash(self) -> int:
        """
        Get the current instance hash

        :return: int, the hash value
        """
        return hash(self)

    @property
    def multi(self) -> bool:

        return om.MFnAttribute(self.attribute()).array

    @property
    def value(self) -> Any:
        """
        Yeah... it s maya commands to get the value of the plug
        This is more flexible than OpenMaya and isn't too demanding

        :return: Any, the value of the current plug
        """

        # TODO: start with check for the attribute
        #  and then check for multiInstances
        apiType = self.attribute().apiType()

        # search for matrices
        if apiType == om.MFn.kTypedAttribute:
            fn_typed = om.MFnTypedAttribute(self.attribute()).attrType()
            if fn_typed == om.MFnData.kMatrix:
                matrix = cmds.getAttr(self.name())
                return om.MMatrix(matrix)

        elif apiType == om.MFn.kMatrixAttribute:
            return om.MMatrix(cmds.getAttr(self.name()))

        # search for vectors
        elif apiType in [om.MFn.kAttribute3Float, om.MFn.kAttribute3Double]:
            return om.MVector(*cmds.getAttr(self.name()))

        return cmds.getAttr(self.name())

    @value.setter
    def value(self, value: Any) -> None:
        """
        Set the value of the current plug

        :param value: Any, the value to set the plug to

        """

        self.set(value)

    @property
    def type(self):
        """
        Get the type of attribute this plug represents

        :return: str, the type of attribute this plug represents
        """

        return cmds.getAttr(self.name(), type=True)


# TODO: Update PlugArray properties and dunders
class PlugArray(om.MPlugArray):

    def __getitem__(self, *args, **kwargs) -> 'Plug':
        return Plug(super().__getitem__(*args, **kwargs))

    """
    def __add__(): ...

    def __contains__(): ...

    def __delitem__(): ...

    def __iadd__(): ...

    def __imul__(): ...

    def __init__(): ...

    def __len__(): ...

    def __mul__(): ...

    def __repr__(): ...

    def __rmul__(): ...

    def __setitem__(): ...

    def __str__(): ...

    def append(): ...

    def clear(): ...

    def copy(): ...

    def insert(): ...

    def remove(): ...

    def setLength(): ...
    """


PlugType = Type[Union[str, Plug]]
PlugArrayType = Type[Union[str, PlugArray]]
