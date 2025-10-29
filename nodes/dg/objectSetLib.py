from typing import List, Any, Union

from ... import cmds
from maya.api import OpenMaya as om

from ...core.abstract.dgLib import DGNode
from ...core.graphLib import Graph
from ...core.nodeRegistry import NodeRegistry


class ObjectSet(DGNode):

    _NODE_TYPE = "objectSet"
    _API_TYPE = om.MFn.kSet

    @property
    def mfnSet(self) -> om.MFnSet:
        """
        Get MFnSet of the om.MObject

        Returns:
            om.MFnSet: the objectSet object
        """
        return om.MFnSet(self)

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

        otherSet = Graph.ls(other)[0]
        return Graph(self.mfnSet.getUnion(otherSet))

    def __sub__(self, other: Union[str, om.MObject]) -> Graph:
        """
        An operation between two sets which returns the members
        of the first set that are not in the second set

        Args:
            other: str | om.MObject, another object set to do the operation

        Returns:
             Graph: a list of nodes
        """

        otherSet = Graph.ls(other)[0]

        return Graph.ls(*cmds.sets(otherSet.name, subtract=self.name))

    def __isub__(self, value: Union[List, str, om.MObject, Graph]):

        if isinstance(value, self.__class__):
            value = value.members

        nodes = Graph.ls(*value)

        self.removeMembers(*nodes)
        return self

    def __iadd__(self, value: Union[List, str, om.MObject, Graph]):

        if isinstance(value, self.__class__):
            value = value.members

        nodes = Graph.ls(*value)

        self.addMembers(nodes)
        return self

    @property
    def size(self) -> int:
        """
        Get the number of members

        Returns:
            int: the number of members
        """

        return self.mfnSet.getMembers(False).length()

    @property
    def members(self) -> Graph:
        """
        Get the set members as cmdo objects

        """

        return Graph(self.mfnSet.getMembers(False))

    @property
    def allMembers(self) -> Graph:
        """
        Get the set members recursively as cmdo objects

        """

        return Graph(self.mfnSet.getMembers(True))

    def copy(self) -> om.MObject:
        """
        Create a new set that is the copy of this set
        Returns:
            om.MObject: a new object set
        """

        return self.__class__(cmds.sets(copy=self.name))

    def flatten(self) -> None:
        """
        Flattens the current set
        """

        cmds.sets(flatten=self.name)

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
            cmds.sets(*Graph.ls(value).getSelectionStrings(), split=self.name)
        )

    def isMember(self, value: Union[List, str, om.MObject]):
        """
        Check if the given node(s) are all part of this set

        Args:
            value: List | str | om.MObject, the name of the node(s)
        """

        cmds.sets(*Graph.ls(value).getSelectionStrings(), isMember=self.name)

    def anyMember(self, value: Union[List, str, om.MObject]):
        """
        Check if any of the given node(s) are part of this set

        Args:
            value: List | str | om.MObject, the name of the node(s)
        """

        cmds.sets(*Graph.ls(value).getSelectionStrings(), anyMember=self.name)

    def addMembers(self, value: Union[List, str, om.MObject, Graph]) -> None:
        """
        Add members to set

        Args:
            value: List | str | om.MObject, the name of the node(s)
        """

        cmds.sets(*Graph.ls(value).getSelectionStrings(), addElement=self.name)

    def removeMembers(self, value: Union[List, str, om.MObject]):
        """
        Remove members from set

        Args:
            value: List | str | om.MObject, the name of the node(s)
        """

        cmds.sets(*Graph.ls(value).getSelectionStrings(), remove=self.name)


class ShadingEngine(ObjectSet):

    _NODE_TYPE = "shadingEngine"
    _API_TYPE = om.MFn.kShadingEngine


NodeRegistry()[ObjectSet.nodeType()] = ObjectSet
NodeRegistry()[ShadingEngine.nodeType()] = ShadingEngine
