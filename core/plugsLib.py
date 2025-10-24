from typing import Union, Any

import math

from maya import cmds
from maya.api import OpenMaya as om


class Plug(om.MPlug):

    def __hash__(self) -> int:
        """
        Make hash using long name and uuid to try having a unique hash
        We "cache" the hash to avoid it changing in the middle of maya operation
        """
        if hasattr(self, '_HASH'):
            return self._HASH

        self._HASH = self.node().hash + hash(self.name())
        return self._HASH

    def __getitem__(self, value: Union[int, str]) -> 'Plug':
        """
        __getitem__ implementation
            - plug["childPlug"]
            - plug[1]

        Args:
            value: int | str, name or index of the child or multi attribute

        Returns:
            om.MPlug: retrieve the asked plug
        """

        # implement str input (for child version)
        if isinstance(value, str):
            for idx in range(self.numChildren()):

                child = self.child(idx)
                afn = om.MFnAttribute(child.attribute())

                if value in [afn.name, afn.shortName]:
                    return self.__class__(child)

        # implement int input can be array if attribute
        # is array else try to compute child plug
        elif isinstance(value, int):
            if self.multi:
                return self.__class__(self.elementByLogicalIndex(value))

            elif self.isCompound:
                return self.__class__(self.child(value))

        return self.__class__()

    def __str__(self) -> str:
        selList = om.MSelectionList()
        selList.add(self)

        return selList.getSelectionStrings()[0]

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

    def get(self, keyname: Union[int, str]) -> 'Plug':
        """
        Get the wanted plug from its name
        plug.get("childPlug")

        Args:
            keyname: int | str, index or name of the asked plug

        Returns:
            om.MPlug: found plug or null plug if not found

        """
        mfn = om.MFnDependencyNode(self.node())

        if mfn.hasAttribute(keyname):
            return self[keyname]

        raise AttributeError(f'{mfn.name()} does not have attribute {keyname}')

    def __setitem__(self, key: str, value: Any) -> None:

        # TODO: need to fix this part with the * operator
        if isinstance(value, (tuple, list)):
            self[key].set(*value)

        else:
            self[key].set(value)

    def set(self, *value: Any) -> None:
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
                matobj = matrixData.create(value)
                self.setMObject(matobj)

            except Exception:
                raise AttributeError(
                    f'{self.name()}, Wrong input type to set matrix attribute'
                    f'Got:'
                    f'\t- type: {type(value)} '
                    f'\t- len: {len(value)} '
                    f'\t- value: {value}'
                )

    def __rshift__(self, other: 'Plug') -> None:
        self.connect(other)

    def __lshift__(self, other: 'Plug') -> None:
        other.connect(self)

    def __truediv__(self, other: om.MPlug) -> None:
        """
        Implement "/" symbol for disconnecting plugs
        Works in either direction: plug1 / plug2 OR plug2 / plug1

        Args:
            other: om.MPlug, a plug to disconnect
        """

        if not isinstance(other, self.__class__):
            other = Plug(other)

        if other.source() == self:
            self.disconnect(other)

        elif self.source() == other:
            other.disconnect(self)

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

    def child(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        return self.__class__(super().child(*args, **kwargs))

    def source(self) -> 'Plug':
        """
        Get the source of the plug

        Returns:
            Plug: source of the plug

        """
        return self.__class__(super().source())

    def destinations(self, *args, **kwargs) -> 'PlugArray':
        """
         Get the destinations of the plug

        Returns:
            PlugArray: an array of destination plugs

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

        Returns:
             int: the hash value
        """
        return hash(self)

    @property
    def multi(self) -> bool:
        mfn = om.MFnAttribute(self.attribute())
        return mfn.array

    @property
    def value(self) -> Any:
        """
        Yeah... it s maya commands to get the value of the plug
        This is more flexible than OpenMaya and isn't too demanding

        Returns:
             Any: the value of the current plug
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

        Args:
            value: Any, the value to set the plug to

        """

        self.set(value)

    @property
    def type(self):
        """
        Get the type of attribute this plug represents

        Returns:
            str: the type of attribute this plug represents
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