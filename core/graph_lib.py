from typing import Any, Union

from maya import cmds as mc
from maya.api import OpenMaya as om

from . import plugs_lib

from .abstract import node_lib
from .abstract import dg_lib
from .abstract import dag_lib

from .node_registry import NodeRegistry
from .exceptions import CmdoException


class Graph(om.MSelectionList):

    __nodeRegistry = NodeRegistry()

    @staticmethod
    def __filter_objects(obj: str | om.MObject) -> str:
        """
        Filter function to convert the input node to str name for maya commands

        Args:
             obj: str | om.MObject, a maya node to convert

        Returns:
            str: the name of the node
        """
        if isinstance(obj, om.MObject):
            return om.MFnDependencyNode(obj).name()

        return obj

    @classmethod
    def __initRegistered(cls, value: om.MObject | str, default=node_lib.Node, **kwargs) -> Any:
        """
        Get node class instance from type

        Args:
            value: om.MObject | str, MObject or name
            default: om.MObject, the default object if nothing is found in
                NodeRegistry

        Returns:
            om.MObject: a subclass of node_lib.Node
        """

        return cls.__nodeRegistry.get(value, default)(value, **kwargs)

    @classmethod
    def ls(cls, *args, **kwargs) -> 'Graph':
        """
        This function is a reimplementation of the mc.ls function

        allow user to gather nodes from string list
        args and kwargs work like mc.ls command

        """

        objects = list(map(cls.__filter_objects, args))

        result = mc.ls(*objects, **kwargs) or []
        lst = cls()
        for item in result:
            lst.add(item)

        return lst

    def createNode(self, typ: str, name=None, parent=None, **kwargs) -> om.MObject:
        """
        This function allow node creation from Graph
        created node will be added to graph

        :param typ: str, type of the created node
        :param name: str, name of the created node
        :param parent: node_lib.Node, parent of the created node

        :return: subclass of node_lib.Node created Node
        """

        try:
            if parent:
                obj = om.MFnDagNode().create(typ, name=name, parent=parent)
                default_object = dag_lib.DAGNode
            else:
                obj = om.MFnDependencyNode().create(typ, name)
                default_object = dg_lib.DGNode

        except RuntimeError as re:
            raise CmdoException(
                f'Could not create node: Node(type={typ}, {name=}, {parent=})'
            ) from re

        self.add(obj)

        return self.__initRegistered(obj, default=default_object, **kwargs)

    @classmethod
    def delete(cls, *args, **kwargs):
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

        result = mc.listHistory(*objects, **kwargs) or []

        lst = cls()
        for item in result:
            lst.add(item)

        return lst

    @classmethod
    def listRelatives(cls, *args, **kwargs) -> 'Graph':
        """
        desc: this function is a reimplementation of the mc.listHistory function
        allow user to gather nodes from string list
        args and kwargs work like mc.listHistory command
        """

        objects = list(map(cls.__filter_objects, args))

        result = mc.listRelatives(*objects, **kwargs) or []

        lst = cls()
        for item in result:
            lst.add(item)

        return lst

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
    def getChildren(cls, node, graph) -> 'Graph':

        node = node_lib.Node(node)
        if not node.hasFn(om.MFn.kDagNode):
            return

        if isinstance(graph, om.MSelectionList):
            graph = cls(graph)

        elif isinstance(graph, list):
            tmp = Graph()

            for node in graph:
                tmp.add(node)

            graph = tmp

        else:
            raise TypeError('graph need to be list or om.MSelectionList')

        # clear graph
        if node in graph:
            node_graph = Graph()
            node_graph.add(node)
            graph = graph - node_graph

        childrens = cls()
        for other in graph:
            otherDagNode = om.MFnDagNode(other)

            if otherDagNode.isChildOf(node):
                childrens.add(other)

        return childrens

    @classmethod
    def getParents(cls, node, graph) -> 'Graph':

        node = node_lib.Node(node)

        if isinstance(graph, om.MSelectionList):
            graph = cls(graph)

        elif not node.hasFn(om.MFn.kDagNode):
            return

        elif isinstance(graph, list):
            tmp = Graph()

            for node in graph:
                tmp.add(node)

            graph = tmp

        else:
            raise TypeError(
                'second argument need to be list or om.MSelectionList')

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

    def __str__(self) -> str:
        args = ', '.join([f'"{x}"' for x in self])
        return f'{self.__class__.__name__} [{args}]'

    def __repr__(self) -> str:
        args = ', '.join([f'"{x}"' for x in self])
        return f'{self.__class__.__name__}.ls({args})'

    def __len__(self) -> int:
        return self.length()

    def get(self, value: Union[str, int]) -> Any:
        return self[value]

    def __getitem__(self, value):

        item = self.getDependNode(value)
        if item.hasFn(om.MFn.kDagNode):
            name = om.MFnDagNode(item).partialPathName()
            default_object = dag_lib.DAGNode

        else:
            name = om.MFnDependencyNode(item).name()
            default_object = dg_lib.DGNode

        return self.__initRegistered(name, default=default_object)

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

    def __iter__(self) -> Union[Any, plugs_lib.Plug]:
        for idx in range(self.length()):
            yield self.get(idx)

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
