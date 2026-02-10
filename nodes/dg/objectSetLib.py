from typing import List, Any, Union

from ... import cmds
from maya.api import OpenMaya as om

from ...core.cmdoTyping import CmdoObject
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

        :return: om.MFnSet, the objectSet object
        """

        return om.MFnSet(self)

    def __add__(self, other: CmdoObject) -> Graph:
        """
        An operation that returns a list of all the members of all sets listed

        :param other: CmdoObject, another object set to do the operation

        :return: Graph: a list of nodes
        """

        otherSet = Graph.ls(other)[0]
        return Graph(self.mfnSet.getUnion(otherSet))

    def __sub__(self, other: CmdoObject) -> Graph:
        """
        An operation between two sets which returns the members
        of the first set that are not in the second set

        :param other: CmdoObject, another object set to do the operation

        :return: Graph: a list of nodes
        """

        otherSet = Graph.ls(other)[0]

        return Graph.ls(*cmds.sets(otherSet.name, subtract=self.name))

    def __isub__(self, value: Union[List, str, om.MObject, Graph]) -> 'ObjectSet':
        """

        :param value:

        :return:
        """

        if isinstance(value, self.__class__):
            value = value.members

        nodes = Graph.ls(*value)
        self.removeMembers(*nodes)
        return self

    def __iadd__(self, value: Union[List, str, om.MObject, Graph]) -> 'ObjectSet':
        """

        :param value:

        :return:
        """

        if isinstance(value, self.__class__):
            value = value.members

        nodes = Graph.ls(*value)
        self.addMembers(nodes)
        return self

    def __len__(self):
        return self.mfnSet.getMembers(False).length()

    @property
    def size(self) -> int:
        """
        Get the number of members

        :return: int, the number of members
        """

        return len(self)

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
        
        :return: om.MObject, a new object set
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

        :param value: Union[List, str, om.MObject], node or list of nodes to split

        :return: om.MObject, a new set containing the list of nodes
        """

        return self.__class__(
            cmds.sets(*Graph.ls(value).getSelectionStrings(), split=self.name)
        )

    def isMember(self, value: Union[List, str, om.MObject]):
        """
        Check if the given node(s) are all part of this set

        :param value: Union[List, str, om.MObject], the name of the node(s)
        """

        cmds.sets(*Graph.ls(value).getSelectionStrings(), isMember=self.name)

    def anyMember(self, value: Union[List, str, om.MObject]):
        """
        Check if any of the given node(s) are part of this set

        :param value: Union[List, str, om.MObject], the name of the node(s)
        """

        cmds.sets(*Graph.ls(value).getSelectionStrings(), anyMember=self.name)

    def addMembers(self, value: Union[List, str, om.MObject, Graph], force=False) -> None:
        """
        Add members to set

        :param value: Union[List, str, om.MObject], the name of the node(s)
        :param force: bool, force the addition of the members to this set
        """
        value = value if isinstance(value, (Graph, list)) else [value]
        if not force:
            cmds.sets(*Graph.ls(*value).getSelectionStrings(), addElement=self.name)

        else:
            cmds.sets(*Graph.ls(*value).getSelectionStrings(), forceElement=self.name)

    def removeMembers(self, value: Union[List, str, om.MObject]):
        """
        Remove members from set

        :param value: Union[List, str, om.MObject], the name of the node(s)
        """

        cmds.sets(*Graph.ls(value).getSelectionStrings(), remove=self.name)


class ShadingEngine(ObjectSet):

    _NODE_TYPE = "shadingEngine"
    _API_TYPE = om.MFn.kShadingEngine

    def assignToMesh(self, value):
        cmds.sets(value, edit=True, forceElement=self.name)


NodeRegistry()[ObjectSet.nodeType()] = ObjectSet
NodeRegistry()[ShadingEngine.nodeType()] = ShadingEngine
