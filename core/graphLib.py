from typing import Any, Union, List, Type

from maya import cmds as mc
from maya.api import OpenMaya as om

from . import plugsLib

from .abstract import nodeLib
from .abstract import dgLib
from .abstract import dagLib

from .nodeRegistry import NodeRegistry
from .exceptions import CmdoException


# TODO: add pop methods etc


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
    def __filter_objects(obj: Union[str, om.MObject, om.MFnDependencyNode, om.MPlug]) -> str:
        """
        Filter function to convert the input node to str name for maya commands

        Args:
             obj: str | MObject, a maya node to convert

        Returns:
            str: the name of the node
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
    def __initRegistered(cls, value: Union[str, om.MObject], default: om.MObject = nodeLib.Node, **kwargs) -> Any:
        """
        Get node class instance from type

        Args:
            value: MObject | str, MObject or name
            default: MObject, the default object if nothing is found in
                NodeRegistry

        Returns:
            MObject: a subclass of nodeLib.Node
        """

        return cls.__nodeRegistry.get(value, default)(value, **kwargs)

    @classmethod
    def __createList(cls, data: List) -> 'Graph':
        """

        Args:
            data: list, a list of data to add to the graph

        Returns:
            Graph: a graph containing the given data
        """
        lst = cls()
        for item in data:
            lst.add(item)

        return lst

    @classmethod
    def ls(cls, *args, **kwargs) -> 'Graph':
        """
        This function is a reimplementation of the mc.ls function

        allow user to gather nodes from string list
        args and kwargs work like mc.ls command

        """

        objects = list(map(cls.__filter_objects, args))

        # remove the long flag if it is present in kwargs
        if kwargs.get(key := 'long') or kwargs.get(key := 'l'):
            kwargs.pop(key)

        result = mc.ls(*objects, long=True, **kwargs) or []
        return cls.__createList(result)

    def createNode(self, typ: str, name=None, parent=None, **kwargs) -> om.MObject:
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
                default_object = dagLib.DAGNode
            else:
                obj = om.MFnDependencyNode().create(typ, name)
                default_object = dgLib.DGNode

        except RuntimeError as re:
            raise CmdoException(
                f'Could not create node: Node(type={typ}, {name=}, {parent=})'
            ) from re

        self.add(obj)

        return self.__initRegistered(obj, default=default_object, **kwargs)

    @classmethod
    def delete(cls, *args, **kwargs) -> None:
        """
        Reimplementation of the delete command

        """

        objs_to_delete = cls.ls(*args, **kwargs)
        for obj in objs_to_delete:
            om.MGlobal.deleteNode(obj)

    @classmethod
    def listHistory(cls, *args, **kwargs) -> 'Graph':
        """
        desc: this function is a reimplementation of the mc.listHistory function
        allow user to gather nodes from string list
        args and kwargs work like mc.listHistory command
        """

        objects = list(map(cls.__filter_objects, args))
        # remove the fullNodeName flag if it is present in kwargs
        if kwargs.get(key := 'fullNodeName') or kwargs.get(key := 'fnn'):
            kwargs.pop(key)

        result = mc.listHistory(*objects, fullNodeName=True, **kwargs) or []
        return cls.__createList(result)

    @classmethod
    def listRelatives(cls, *args, **kwargs) -> 'Graph':
        """
        desc: this function is a reimplementation of the mc.listHistory function
        allow user to gather nodes from string list
        args and kwargs work like mc.listHistory command
        """

        objects = list(map(cls.__filter_objects, args))

        # remove the fullPath flag if it is present in kwargs
        if kwargs.get(key := 'fullPath') or kwargs.get(key := 'f'):
            kwargs.pop(key)

        result = mc.listRelatives(*objects, fullPath=True, **kwargs) or []
        return cls.__createList(result)

    @classmethod
    def listConnections(cls, *args, **kwargs) -> 'Graph':
        """
        Reimplementation of the listConnections command

        """
        objects = list(map(cls.__filter_objects, args))

        # remove the fullNodeName flag if it is present in kwargs
        if kwargs.get(key := 'fullNodeName') or kwargs.get(key := 'fnn'):
            kwargs.pop(key)

        result = mc.listConnections(*objects, fullNodeName=True, **kwargs) or []
        return cls.__createList(result)

    @classmethod
    def getDagRoots(cls, nodes, safe=True) -> 'Graph':
        """
        This method get dag root from given nodes

        Args:
            nodes: nodes you want dag roots on
            safe: raise an error or not

        Returns:
            Graph: the founded relative dagRoots
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

            is_child = False
            mfnDagNode = om.MFnDagNode(item)
            for other in nodes - previous:
                if other.hasFn(om.MFn.kDagNode):
                    is_child |= mfnDagNode.isChildOf(other)

            if not is_child:
                roots.add(item)

        return roots

    @classmethod
    def getChildren(cls, node, graph) -> Union['Graph', None]:
        """
        Get all children of node

        Args:
            node: node to get children for
            graph: the graph to search in

        Returns:
            Graph: a Graph object holding node children
        """

        node = nodeLib.Node(node)
        if not node.hasFn(om.MFn.kDagNode):
            return None

        if isinstance(graph, om.MSelectionList):
            graph = cls(graph)

        elif isinstance(graph, list):
            tmp = Graph()

            for node in graph:
                tmp.add(node)

            graph = tmp

        else:
            raise TypeError('graph need to be list or MSelectionList')

        # clear graph
        if node in graph:
            node_graph = Graph()
            node_graph.add(node)
            graph = graph - node_graph

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

        Args:
            node: node to get parents for
            graph: the graph to search in

        Returns:
            Graph: a Graph object holding node parents
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
            node_graph = Graph()
            node_graph.add(node)
            graph = graph - node_graph

        dagNode = om.MFnDagNode(node)

        parents = cls()
        for other in graph:

            if dagNode.isChildOf(other):
                parents.add(other)

        return parents

    @classmethod
    def select(cls, *args, **kwargs):
        """
        Reimplementation of the select command

        """
        objects = list(map(cls.__filter_objects, args))

        mc.select(*objects, **kwargs)

    @classmethod
    def duplicate(cls, *args, **kwargs):
        """
        Reimplementation of the duplicate command

        """
        objects = list(map(cls.__filter_objects, args))

        # remove the fullPath flag if it is present in kwargs
        if kwargs.get(key := 'fullPath') or kwargs.get(key := 'f'):
            kwargs.pop(key)

        result = mc.duplicate(*objects, fullPath=True, **kwargs)

        return cls.__createList(result)

    def pop(self, value) -> om.MObject: ...  # TODO

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

    def get(self, value: Union[str, int]) -> Any:
        return self[value]

    def __getitem__(self, value):
        if isinstance(value, slice):
            newGraph = self.__class__()
            for index in range(*value.indices(len(self))):
                newGraph.add(self[index])

            return newGraph

        mItSel = om.MItSelectionList(self)
        for i in range(value + 1):
            if i != value:
                mItSel.iternext()
                continue

            if mItSel.itemType() == mItSel.kPlugSelectionItem:
                return plugsLib.Plug(mItSel.getPlug())

        item = self.getDependNode(value)
        if item.hasFn(om.MFn.kDagNode):
            name = om.MFnDagNode(item).partialPathName()
            default_object = dagLib.DAGNode

        else:
            name = om.MFnDependencyNode(item).name()
            default_object = dgLib.DGNode

        return self.__initRegistered(name, default=default_object)

    def __setitem__(self, key, value):

        item = self.ls(value)[0]

        self.replace(key, item)

    def __and__(self, other: om.MSelectionList) -> 'Graph':
        """
        intersection "&" symbol
        """
        if not isinstance(other, om.MSelectionList):
            raise TypeError(f'can not intersect Graph and {type(other)}')

        copy = self.__class__().copy(self)
        return copy.intersect(other)

    def __or__(self, other: om.MSelectionList) -> 'Graph':
        """
        union "|" symbole
        """
        if not isinstance(other, om.MSelectionList):
            raise TypeError(f'can not unify Graph and {type(other)}')

        self_copy = self.__class__().copy(self)
        other_copy = self.__class__().copy(other)

        return self_copy.merge(other_copy)

    def __xor__(self, other: om.MSelectionList) -> 'Graph':
        """
        symmetrical difference "^" symbole

        """
        copy = self.__class__().copy(self)
        return copy.merge(other, strategy=om.MSelectionList.kXORWithList)

    def __iter__(self) -> Any:
        for value in range(self.length()):
            yield self.get(value)

    def __contains__(self, item: Union[om.MObject, Any, str]) -> bool:

        item_obj = None
        if isinstance(item, om.MObject):
            item_obj = item

        elif isinstance(item, self.__nodeRegistry.get('default')):
            item_obj = item

        elif isinstance(item, str):
            tmp_graph = self.__class__.ls(item)
            if tmp_graph and tmp_graph[0].exists:
                item_obj = tmp_graph.getDependNode(0)
        else:
            raise TypeError(f'can not get MObject from {item}')

        return self.hasItem(item_obj) if item_obj else False

        # return self.hasItem(item_obj)

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
        Args:
            other: Any, objects to add to the graph

        Returns:
            Graph: returns the current instance with added nodes
        """

        # if isinstance(other, om.MSelectionList):
        #     other = [obj for obj in self.__class__.ls(other)]

        objects = list(map(self.__filter_objects, other))

        result = mc.ls(*objects) or []
        for item in result:
            self.add(item)

        return self

    def __isub__(self, other: Any) -> 'Graph':
        """
        Implement "-=" operation
        Args:
            other: Any, objects to remove from the graph

        Returns:
            Graph: returns the current instance with removed nodes
        """
        return self.merge(other, strategy=om.MSelectionList.kRemoveFromList)
