from typing import Union, List, Dict, Optional, Type

from maya import cmds
from maya.api import OpenMaya as om

from ...core.plugsLib import Plug
from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry
from ...core.graphLib import Graph


class Container(dgLib.DGNode):

    _NODE_TYPE = "container"
    _API_TYPE = om.MFn.kContainerBase

    @classmethod
    def containerize(cls, graph: Graph, name: str = None, setRootTransform: bool = False) -> om.MObject:

        container = cls.create(name)
        for node in graph:
            container.addNode(node)

        if setRootTransform:
            if dagRoots := graph.dagRoots:
                container.rootTransform = dagRoots.get(0)

        return container

    def __str__(self) -> str:
        return self.name

    def __getitem__(self, value) -> Plug:
        """
        Convenient implementations to retrieve a plug from the current node

        :return: Plug, the wanted plug
        """

        plugs, names = self.mfnContainer.getPublishedPlugs()
        for plug, name in zip(plugs, names):
            if value == name:
                return Plug(plug)

        return Plug(self.dependencyNode.findPlug(value, True))

    @property
    def mfnContainer(self):

        """
        Return an MFnContainerNode object

        :return: om.MFnContainerNode, MFnContainerNode object
        """

        return om.MFnContainerNode(self)

    @property
    def parent(self) -> Optional['Container']:
        """
        Get the parent container

        :return: Container, the parent container
        """

        parent = self.mfnContainer.getParentContainer()
        if parent and not parent.isNull():
            return None

        return self.__class__(parent)

    @property
    def children(self) -> List['Container']:
        """
        Get the child containers

        :return: Container, the parent container
        """
        return_list = []
        for item in self.mfnContainer.getSubcontainers():
            return_list.append(self.__class__(item))

        return return_list

    @property
    def nodes(self) -> Graph:

        """
        Get container nodes

        :return: Graph, the list of contained nodes
        """

        sel = Graph()
        for item in self.mfnContainer.getMembers():
            sel.add(item)

        return sel

    def __publishedNodes(self, attr) -> Dict[str, dgLib.DGNode]:
        """
        Get container published nodes

        :return: Graph, the list of published nodes
        """
        names, nodes = self.mfnContainer.getPublishedNodes(attr)
        return dict(zip(names, Graph.ls(nodes)))

    @property
    def publishedParentAnchor(self) -> Dict[str, dgLib.DGNode]:
        """
        Get container published parent anchors

        :return: Graph, the list of published parent anchors
        """
        return self.__publishedNodes(self.mfnContainer.kParentAnchor)

    @property
    def publishedChildAnchor(self) -> Dict[str, dgLib.DGNode]:
        """
        Get container published child anchors

        :return: Graph, the list of published child anchors
        """
        return self.__publishedNodes(self.mfnContainer.kChildAnchor)

    @property
    def publishedNodes(self) -> Dict[str, dgLib.DGNode]:
        """
        Get container published generic anchors

        :return: Graph, the list of published generic anchors
        """
        return self.__publishedNodes(self.mfnContainer.kGeneric)

    @property
    def publishedPlugs(self) -> Dict[str, Plug]:
        """
        Get container published plugs

        :return: Graph, the list of published plugs
        """
        plugs, names = self.mfnContainer.getPublishedPlugs()
        plugs = [Plug(plug) for plug in plugs]
        return dict(zip(names, plugs))

    @property
    def current(self) -> bool:

        """
        Is the current container

        :return: bool, is the current container
        """

        return self.mfnContainer.isCurrent()

    @current.setter
    def current(self, current: bool) -> None:

        """
        Set as the current container

        """

        self.mfnContainer.makeCurrent(current)

    @property
    def rootTransform(self) -> dgLib.DGNode:

        """
        Get the root transform of the container

        :return: dgLib.DGNode, an instance of a subclass of Node
        """
        return Graph.ls(self.mfnContainer.getRootTransform())[0]

    @rootTransform.setter
    def rootTransform(self, node: Union[str, dgLib.DGNode, None]) -> None:

        """
        Set the root transform of the container

        """

        if node is None:
            source_plug = self['rootTransform'].source()
            if source_plug.isNull:
                return

            container_plug = Graph.ls(self.name)['rootTransform']
            Plug(source_plug).disconnect(container_plug)
            return

        node = Graph.ls(node)[0]
        if node not in self.nodes:
            raise NameError(f'{node} is not part of the container')

        node['message'] >> self['rootTransform']

    def createNode(self, typ, name=None, parent=None) -> om.MObject:
        """
        Create a node and add it to the container

        :return: dgLib.DGNode, an instance of a subclass of Node
        """
        node = Graph().createNode(typ, name=name, parent=parent)

        self.addNode(node)

        return node

    def addNode(self, node: Union[str, om.MObject]) -> None:

        """
        Add given node to the container

        """
        
        node = Graph.ls(node)[0]
        cmds.container(self.name, addNode=node.name, edit=True)


NodeRegistry()[Container.nodeType()] = Container
