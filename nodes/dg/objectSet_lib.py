from typing import List, Any, Union

from maya.api import OpenMaya as om
from maya import cmds as mc

from ...core.abstract import dg_lib
from ...core.node_registry import NodeRegistry


class ObjectSet(dg_lib.DGNode):

    _NODE_TYPE = "objectSet"
    _API_TYPE = om.MFn.kSet

    @staticmethod
    def __getObjectName(obj: Union[str, om.MObject]) -> str:
        """
        Get the name obj the given node

        Args:
             obj: str | om.MObject, a maya node to convert

        Returns:
            str: the name of the node
        """

        if isinstance(obj, om.MObject):
            return om.MFnDependencyNode(obj).name()

        return obj

    def __filterObjects(self, objs: Union[List, str, om.MObject]) -> List[str]:
        """
        Filter function to convert the input node to str name for maya commands

        Args:
             objs: List | str | om.MObject, a maya node or list of maya nodes

        Returns:
            List[str]: a list of node names
        """
        if not isinstance(objs, (tuple, list)):
            objs = [objs]

        return list(map(self.__getObjectName, objs))

    def __init__(self, name: Union[str, om.MObject] = None) -> None:
        """
        Initialize an instance of Set

        Args:
            name: str | om.MObject, the name of the node
        """

        super().__init__(name=name)

    def __add__(self, other):
        """
        An operation that returns a list of all the members of all sets listed

        Args:
            other: str | om.MObject, another object set to do the operation

        Returns:
             List[str]: a list of nodes
        """

        otherSet = self.__getObjectName(other)
        return mc.sets(otherSet, union=self.name)

    def __sub__(self, other: Union[str, om.MObject]) -> List[str]:
        """
        An operation between two sets which returns the members
        of the first set that are not in the second set

        Args:
            other: str | om.MObject, another object set to do the operation

        Returns:
             List[str]: a list of nodes
        """

        otherSet = self.__getObjectName(other)
        return mc.sets(otherSet, subtract=self.name)

    def __isub__(self, value: Union[List, str, om.MObject]):

        if isinstance(value, self.__class__):
            value = value.members

        self.removeMembers(value)
        return self

    def __iadd__(self, value: Union[List, str, om.MObject]):

        if isinstance(value, self.__class__):
            value = value.members

        self.addMembers(value)
        return self

    @property
    def size(self) -> int:
        """
        Get the number of members

        Returns:
            int: the number of members
        """

        return mc.sets(self.name, query=True, size=True)

    @property
    def members(self) -> List[om.MObject]:
        """
        Get the set members as cmdo objects

        """

        nodeNames = mc.sets(self.name, query=True) or []

        return [
            NodeRegistry().get(name, dg_lib.DGNode)(name)
            for name in nodeNames
        ]

    def copy(self) -> om.MObject:
        """
        Create a new set that is the copy of this set
        Returns:
            om.MObject: a new object set
        """
        return self.__class__(mc.sets(copy=self.name))

    def flatten(self) -> None:
        """
        Flattens the current set
        """

        mc.sets(flatten=self.name)

    def split(self, value: Union[List, str, om.MObject]) -> om.MObject:
        """
        Get a new set with the given nodes
        and remove those nodes from the current set

        Args:
            value: List | str | om.MObject, node or list of nodes to split

        Returns:
            om.MObject: a new set containing the list of nodes
        """

        return self.__class__(
            mc.sets(*self.__filterObjects(value), split=self.name)
        )

    def isMember(self, value: Union[List, str, om.MObject]):
        """
        Check if the given node(s) are all part of this set

        Args:
            value: List | str | om.MObject, the name of the node(s)
        """

        mc.sets(*self.__filterObjects(value), isMember=self.name)

    def anyMember(self, value: Union[List, str, om.MObject]):
        """
        Check if any of the given node(s) are part of this set

        Args:
            value: List | str | om.MObject, the name of the node(s)
        """

        mc.sets(*self.__filterObjects(value), anyMember=self.name)

    def addMembers(self, value: Union[List, str, om.MObject]) -> None:
        """
        Add members to set

        Args:
            value: List | str | om.MObject, the name of the node(s)
        """

        mc.sets(*self.__filterObjects(value), addElement=self.name)

    def removeMembers(self, value: Union[List, str, om.MObject]):
        """
        Remove members from set

        Args:
            value: List | str | om.MObject, the name of the node(s)
        """

        mc.sets(*self.__filterObjects(value), remove=self.name)


NodeRegistry()[ObjectSet.nodeType()] = ObjectSet
