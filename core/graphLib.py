from typing import Any, Union, List, Type, Callable

from .. import cmds, om

from . import plugsLib
from .cmdoTyping import CmdoObject, CmdoList

from .abstract import nodeLib, dgLib, dagLib

from .nodeRegistry import NodeRegistry
from .exceptions import CmdoException, CmdoPlugException


# TODO: find a way to handle f***ing components (ie: vertices, edges, etc)
class Graph(om.MSelectionList):

    __nodeRegistry = NodeRegistry()

    @staticmethod
    def __isSubClass(cls1, cls2):
        """
        We have wierd import because of maya (and other stuff)
        So we can t use the built-in issubclass to check classes
        """

        return repr(cls2) in repr(cls1.__class__.mro())

    @staticmethod
    def __filterObjects(obj: Union[CmdoObject, om.MFnDependencyNode, om.MPlug]) -> str:
        """
        Filter function to convert the input node to str name for maya commands

        :param obj: Union[CmdoObject, om.MFnDependencyNode, om.MPlug], a maya node to convert

        :return: str, the name of the node
        """
        if isinstance(obj, str):
            return obj

        if Graph.__isSubClass(obj, om.MPlug):
            return obj.name()

        if Graph.__isSubClass(obj, om.MObject):
            return om.MFnDependencyNode(obj).name()

        if Graph.__isSubClass(obj, om.MFnDependencyNode):
            return obj.name()

        if isinstance(obj, Graph):
            return obj.getSelectionStrings()

        return str(obj)

    @classmethod
    def __initRegistered(cls, value: CmdoObject, default: om.MObject = nodeLib.Node, **kwargs) -> Any:
        """
        Get node class instance from type

        :param value:CmdoObject, MObject or name
        :param default: MObject, the default object if nothing is found in NodeRegistry

        :return: MObject: a subclass of nodeLib.Node
        """

        return cls.__nodeRegistry.get(value, default)(value, **kwargs)

    @classmethod
    def __createList(cls, data: List) -> 'Graph':
        """

        :param data: list, a list of data to add to the graph

        :return: Graph, a graph containing the given data
        """
        graph = cls()
        for item in data:
            graph.add(item)

        return graph

    @classmethod
    def ls(cls, *args, **kwargs) -> 'Graph':
        """
        This function is a reimplementation of the cmds.ls function

        allow user to gather nodes from string list
        args and kwargs work like cmds.ls command

        """

        objects = list(map(cls.__filterObjects, args))

        # remove the long flag if it is present in kwargs
        if kwargs.get(key := 'long') or kwargs.get(key := 'l'):
            kwargs.pop(key)

        result = cmds.ls(*objects, long=True, **kwargs) or []
        return cls.__createList(result)

    @classmethod
    def listHistory(cls, *args, **kwargs) -> 'Graph':
        """
        This function is a reimplementation of the cmds.listHistory function

        allow user to gather nodes from string list
        args and kwargs work like cmds.listHistory command

        """

        objects = list(map(cls.__filterObjects, args))
        # remove the fullNodeName flag if it is present in kwargs
        if kwargs.get(key := 'fullNodeName') or kwargs.get(key := 'fnn'):
            kwargs.pop(key)

        result = cmds.listHistory(*objects, fullNodeName=True, **kwargs) or []
        return cls.__createList(result)

    @classmethod
    def listRelatives(cls, *args, **kwargs) -> 'Graph':
        """
        This function is a reimplementation of the cmds.listHistory function

        allow user to gather nodes from string list
        args and kwargs work like cmds.listHistory command

        """

        objects = list(map(cls.__filterObjects, args))

        # remove the fullPath flag if it is present in kwargs
        if kwargs.get(key := 'fullPath') or kwargs.get(key := 'f'):
            kwargs.pop(key)

        result = cmds.listRelatives(*objects, fullPath=True, **kwargs) or []
        return cls.__createList(result)

    @classmethod
    def listConnections(cls, *args, **kwargs) -> 'Graph':
        """
        Reimplementation of the cmds.listConnections command

        """

        objects = list(map(cls.__filterObjects, args))

        # remove the fullNodeName flag if it is present in kwargs
        if kwargs.get(key := 'fullNodeName') or kwargs.get(key := 'fnn'):
            kwargs.pop(key)

        result = cmds.listConnections(*objects, fullNodeName=True, **kwargs) or []
        return cls.__createList(result)

    @classmethod
    def getHighestNodesInList(cls, nodes: CmdoList, safe: bool = True) -> 'Graph':
        """
        This method get the highest parent nodes in given nodes

        :param nodes: CmdoList, nodes you want dag roots on
        :param safe: bol, raise an error or not

        :return: Graph, the founded relative dagRoots
        """

        if isinstance(nodes, list):
            tmp = Graph()

            for node in nodes:
                tmp.add(node)

            nodes = tmp

        elif isinstance(nodes, om.MSelectionList):
            nodes = cls(nodes)

        previous = cls()
        roots = cls()
        for item in nodes:
            previous.add(item)

            if (not safe) and (not item.hasFn(om.MFnDagNode)):
                raise TypeError(f'{item} is not a dagNode')

            if safe and (not item.hasFn(om.MFn.kDagNode)):
                continue

            isChild = False
            mfnDagNode = om.MFnDagNode(item)
            for other in nodes - previous:
                if other.hasFn(om.MFn.kDagNode):
                    isChild |= mfnDagNode.isChildOf(other)

            if not isChild:
                roots.add(item)

        return roots

    @classmethod
    def getChildren(cls, node, graph) -> 'Graph':
        """
        Get all children of node

        :param node: node to get children for
        :param graph: the graph to search in

        :return: Graph, a Graph object holding node children
        """

        node = nodeLib.Node(node)
        if not node.hasFn(om.MFn.kDagNode):
            return None

        if isinstance(graph, om.MSelectionList):
            graph = cls(graph)

        elif isinstance(graph, list):
            tempGraph = Graph()

            for node in graph:
                tempGraph.add(node)

            graph = tempGraph

        else:
            raise TypeError('graph need to be list or MSelectionList')

        # clear graph
        if node in graph:
            nodeGraph = Graph()
            nodeGraph.add(node)
            graph = graph - nodeGraph

        children = cls()
        for other in graph:
            otherDagNode = om.MFnDagNode(other)

            if otherDagNode.isChildOf(node):
                children.add(other)

        return children

    @classmethod
    def getParents(cls, node, graph) -> Union['Graph', None]:
        """
        Get all parents of node

        :param node: node to get parents for
        :param graph: the graph to search in

        :return: Graph, a Graph object holding node parents
        """

        node = nodeLib.Node(node)

        if isinstance(graph, om.MSelectionList):
            graph = cls(graph)

        elif not node.hasFn(om.MFn.kDagNode):
            return None

        elif isinstance(graph, list):
            tmp = Graph()

            for node in graph:
                tmp.add(node)

            graph = tmp

        else:
            raise TypeError('second argument need to be list or MSelectionList')

        # clear graph
        if node in graph:
            nodeGraph = Graph()
            nodeGraph.add(node)
            graph = graph - nodeGraph

        dagNode = om.MFnDagNode(node)

        parents = cls()
        for other in graph:

            if dagNode.isChildOf(other):
                parents.add(other)

        return parents

    # @classmethod
    # def duplicate(cls, *args, **kwargs):
    #     """
    #     Reimplementation of the cmds.duplicate command
    #
    #     """
    #     objects = list(map(cls.__filterObjects, args))
    #
    #     # remove the fullPath flag if it is present in kwargs
    #     if kwargs.get(key := 'fullPath') or kwargs.get(key := 'f'):
    #         kwargs.pop(key)
    #
    #     result = cmds.duplicate(*objects, fullPath=True, **kwargs)
    #
    #     return cls.__createList(result)

    def createNode(self, typ: str, name: str = None, parent: CmdoObject = None, **kwargs) -> om.MObject:
        """
        This function allow node creation from Graph
        created node will be added to graph

        :param typ: str, type of the created node
        :param name: str, name of the created node
        :param parent: nodeLib.Node, parent of the created node

        :return: subclass of nodeLib.Node created Node
        """

        try:
            if parent:
                obj = om.MFnDagNode().create(typ, name=name, parent=parent)
                defaultObject = dagLib.DAGNode
            else:
                obj = om.MFnDependencyNode().create(typ, name)
                defaultObject = dgLib.DGNode

        except RuntimeError as re:
            raise CmdoException(
                f'Could not create node: Node(type={typ}, {name=}, {parent=})'
            ) from re

        self.add(obj)

        return self.__initRegistered(obj, default=defaultObject, **kwargs)

    def select(self, **kwargs):
        """
        Select the nodes in the current graph

        """

        cmds.select(self, **kwargs)

    def delete(self, **kwargs):
        """
        Delete the nodes in the current graph

        """

        cmds.delete(self, **kwargs)

    def setMembersAttributeValue(self, attr: Union[str, plugsLib.Plug], value: Any, raiseOnError: bool = False) -> None:
        """
        Set attribute for all members if they correspond or have the attribute

        :param attr: Union[str, plugsLib.Plug], the name of the attribute
            or plug to set
        :param value: Any, the value to set the attribute to
        :param raiseOnError: bool, if true raise a CmdoPlugException if
            the attribute is locked or connected

        """
        dgDagType = [
            om.MItSelectionList.kDNselectionItem,
            om.MItSelectionList.kDagSelectionItem
        ]
        plugType = om.MItSelectionList.kPlugSelectionItem

        def isNotSettable(plug: om.MPlug):
            if not plug.isCompound and not plug.isArray:
                return plug.isLocked or plug.isDestination

            elif plug.isCompound:
                return any(
                    plug.child(n).isLocked or plug.child(n).isDestination
                    for n in range(plug.numChildren())
                )
            elif plug.isArray:
                return any(
                    plug.child(n).isLocked or plug.child(n).isDestination
                    for n in range(plug.numElements())
                )

            if raiseOnError:
                raise CmdoPlugException(f'Invalid plug : {plug.name()}')

            return True

        def isValidPlug(item, obj) -> bool:
            return item.itemType() == plugType and obj.name().endswith(attr)

        def isValidObjPlug(item, obj) -> bool:
            return item.itemType() in dgDagType and obj.hasAttr(attr)

        for i, item in enumerate(om.MItSelectionList(self)):
            currentObj = self[i]

            if isValidPlug(item, currentObj):
                if not raiseOnError and isNotSettable(currentObj):
                    continue

                currentObj.value = value

            elif isValidObjPlug(item, currentObj):
                if not raiseOnError and isNotSettable(currentObj[attr]):
                    continue

                currentObj[attr] = value

    def getMembersAttributeValue(self, attr: Union[str, plugsLib.Plug], raiseOnError: bool = False) -> List:
        """
        Get attribute for all members if they correspond or have the attribute

        :param attr: Union[str, plugsLib.Plug], the name of the attribute or
            plug to set
        :param raiseOnError: bool, if true raise a CmdoPlugException if
            the attribute is locked or connected

        """
        dgDagType = [
            om.MItSelectionList.kDNselectionItem,
            om.MItSelectionList.kDagSelectionItem
        ]
        plugType = om.MItSelectionList.kPlugSelectionItem

        def isNotSettable(plug: om.MPlug):
            return plug.isLocked or plug.isConnected

        def isValidPlug(item, obj) -> bool:
            return item.itemType() == plugType and obj.name().endswith(attr)

        def isValidObjPlug(item, obj) -> bool:
            return item.itemType() in dgDagType and obj.hasAttr(attr)

        result = []
        for i, item in enumerate(om.MItSelectionList(self)):
            currentObj = self[i]

            if isValidPlug(item, currentObj):
                if not raiseOnError and isNotSettable(currentObj):
                    continue

                result.append(currentObj.value)

            elif isValidObjPlug(item, currentObj):
                if not raiseOnError and isNotSettable(currentObj[attr]):
                    continue

                result.append(currentObj[attr].value)

        return result

    def pop(self, value: int) -> om.MObject:
        """
        Implement list.pop function

        :param value: int, the index of the item to remove

        :return: om.MObject, the removed item

        """
        # check negative indices
        value = value if value >= 0 else len(self) + value

        itemToReturn = self[value]
        self.remove(value)

        return itemToReturn

    def append(self, value: Union[om.MObject, om.MPlug]) -> None:
        """
        Implement list.append function

        :param value: Union[om.MObject, om.MPlug], the value to append
        """

        self.add(value)

    def extend(self, value: CmdoList) -> 'Graph':
        """
        Add each element of a list to the current graph

        :param value: CmdoList, the list to extend with

        :return: Graph, the current extended list
        """
        objects = list(map(self.__filterObjects, value))

        result = cmds.ls(*objects) if objects else []
        for item in result:
            self.add(item)

        return self

    def filterFromKey(self, filterKey: Callable) -> 'Graph':
        """
        Given a filter key, return a filtered graph

        :param filterKey: Callable, a function to filter the current graph

        :return: Graph, a new filtered graph
        """

        return self.__class__.ls(*fil) if bool(fil := list(filter(filterKey, self))) else self.__class__()

    def __str__(self) -> str:
        args = ', '.join([f'"{x}"' for x in self])
        return f'{self.__class__.__name__} [{args}]'

    def __bool__(self) -> bool:
        return len(self) > 0

    def __repr__(self) -> str:
        args = ', '.join([f'"{x}"' for x in self])
        return f'{self.__class__.__name__}.ls({args})'

    def __len__(self) -> int:
        return self.length()

    def __getattr__(self, attr: Union[str, plugsLib.Plug]) -> List[Any]:
        """
        Get attribute for all members if they correspond or have the attribute

        :param attr: Union[str, plugsLib.Plug], the name of the attribute or
            plug to set

        :return: List[Any], the list of attribute values

        """
        return self.getMembersAttributeValue(attr)

    def __setattr__(self, attr: Union[str, plugsLib.Plug], value: Any) -> None:
        """
        Set attribute for all members if they correspond or have the attribute

        :param attr: Union[str, plugsLib.Plug], the name of the attribute or
            plug to set
        :param value: Any, the value to set the attribute to

        """
        self.setMembersAttributeValue(attr, value)

    def __getitem__(self, value: Union[int, slice]):
        # Implement slicing in Graph
        if isinstance(value, slice):
            newGraph = self.__class__()
            for index in range(*value.indices(len(self))):
                newGraph.add(self[index])

            return newGraph

        # check negative indices
        value = value if value >= 0 else len(self) + value

        # check for plugs
        mItSel = om.MItSelectionList(self)
        for i in range(value + 1):
            if i != value:
                mItSel.iternext()
                continue

            if mItSel.itemType() == mItSel.kPlugSelectionItem:
                return plugsLib.Plug(self.getPlug(i))

        # convert to DAGNode or DGNode
        item = self.getDependNode(value)
        if item.hasFn(om.MFn.kDagNode):
            name = om.MFnDagNode(item).partialPathName()
            defaultObject = dagLib.DAGNode

        else:
            name = om.MFnDependencyNode(item).name()
            defaultObject = dgLib.DGNode

        return self.__initRegistered(name, default=defaultObject)

    def __setitem__(self, key, value):

        item = self.ls(value)[0]

        self.replace(key, item)

    def __and__(self, other: om.MSelectionList) -> 'Graph':
        """
        Intersection "&" symbol
        """

        if not isinstance(other, om.MSelectionList):
            raise TypeError(f'can not intersect Graph and {type(other)}')

        copy = self.__class__().copy(self)
        return copy.intersect(other)

    def __or__(self, other: om.MSelectionList) -> 'Graph':
        """
        Union "|" symbole
        """

        if not isinstance(other, om.MSelectionList):
            raise TypeError(f'can not unify Graph and {type(other)}')

        selfCopy = self.__class__().copy(self)
        otherCopy = self.__class__().copy(other)

        return selfCopy.merge(otherCopy)

    def __xor__(self, other: om.MSelectionList) -> 'Graph':
        """
        Symmetrical difference "^" symbole

        """

        copy = self.__class__().copy(self)
        return copy.merge(other, strategy=om.MSelectionList.kXORWithList)

    def __iter__(self) -> Any:
        for value in range(self.length()):
            yield self[value]

    def __contains__(self, item: Union[om.MObject, Any, str]) -> bool:

        itemObj = None
        if isinstance(item, om.MObject):
            itemObj = item

        elif isinstance(item, self.__nodeRegistry.get('default')):
            itemObj = item

        elif isinstance(item, str):
            tempGraph = self.__class__.ls(item)
            if tempGraph and tempGraph[0].exists:
                itemObj = tempGraph.getDependNode(0)
        else:
            raise TypeError(f'can not get MObject from {item}')

        return self.hasItem(itemObj) if itemObj else False

    def __add__(self, other: om.MSelectionList) -> 'Graph':

        copy = self.__class__().copy(self)
        return copy.merge(other, strategy=om.MSelectionList.kMergeNormal)

    def __sub__(self, other: om.MSelectionList) -> 'Graph':

        # TODO: handle few errors with this one
        #  maybe use the name more than the MObject from the Node
        copy = self.__class__().copy(self)
        return copy.merge(other, strategy=om.MSelectionList.kRemoveFromList)

    def __iadd__(self, other: Any) -> 'Graph':
        """
        Implement "+=" operation

        :param other: Any, objects to add to the graph

        :return: Graph, returns the current instance with added nodes
        """

        # if isinstance(other, om.MSelectionList):
        #     other = [obj for obj in self.__class__.ls(other)]

        objects = list(map(self.__filterObjects, other))

        result = cmds.ls(*objects) or []
        for item in result:
            self.add(item)

        return self

    def __isub__(self, other: Any) -> 'Graph':
        """
        Implement "-=" operation

        :param other: Any, objects to remove from the graph

        :return: Graph, returns the current instance with removed nodes
        """
        return self.merge(other, strategy=om.MSelectionList.kRemoveFromList)


# NodeRegistry._graph = Graph
GraphType = Type[Union[str, Graph]]
