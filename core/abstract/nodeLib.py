from typing import List, Optional, Union, Any, Tuple, Dict, Type

from maya import cmds
from maya.api import OpenMaya as om

from ..cmdoTyping import CmdoObject
from ..exceptions import CmdoException, CmdoPlugException
from ..plugsLib import Plug, PlugArray


class Node(om.MObject):

    # Needs to be filled in subClasses to be added to NodeRegistry
    # This enables cmdo to create and get those nodes using graphLib
    _NODE_TYPE = None
    _API_TYPE = None

    @classmethod
    def openMayaType(cls) -> int:
        """
        Internal OpenMaya type

        :return: int, the OpenMaya type
        """

        return cls._API_TYPE

    @classmethod
    def nodeType(cls) -> str:
        """
        Internal cmds type

        :return: str, the cmds type
        """

        return cls._NODE_TYPE

    @classmethod
    def getExcludedMembers(cls) -> Tuple[List[str], List[str]]:
        """
        Get a list of excluded members for the "printClass" function

        """

        do_not_print_types = [
            'method_descriptor', 'mappingproxy', 'type', 'wrapper_descriptor',
            "<class 'dict'>", 'getset_descriptor', 'builtin_function_or_method',
            'method-wrapper'
        ]
        do_not_print_names = ['__module__', '__str__', '__doc__', '__weakref__']

        return do_not_print_types, do_not_print_names

    @classmethod
    def create(cls, name: str = None, parent: CmdoObject = None) -> om.MObject:

        """
        Create a new instance of this class

        :param name: str, an optional name for the new node
        :param parent: CmdoObject, an optional parent for the new node

        :return: om.MObject, the created object (subclass of om.MObject)
        """

        try:
            if parent:
                obj = om.MFnDagNode().create(cls.nodeType(), name=name, parent=parent)
            else:
                obj = om.MFnDependencyNode().create(cls.nodeType(), name)

        except RuntimeError as re:
            raise CmdoException(
                f'Could not create node: Node(type={cls.nodeType()}, {name=}, {parent=})'
            ) from re

        return cls(obj)

    def __init__(self, name: CmdoObject = None) -> None:

        """
        Initialize an instance of Node

        :param name: CmdoObject, the name of the node
        """

        if isinstance(name, str):

            sel_list = om.MSelectionList()
            sel_list.add(name)
            super().__init__(sel_list.getDependNode(0))

        elif isinstance(name, om.MObject):
            super().__init__(name)

        self.__dependencyNode = om.MFnDependencyNode(self)

    def __hash__(self) -> int:
        """
        Make hash using long name and uuid to try having a unique hash

        We "cache" the hash to avoid it changing in the middle of maya operation
        """

        if not hasattr(self, '_HASH'):
            self._HASH = None

        if self._HASH is None:
            self._HASH = (
                    hash(self.dependencyNode.uniqueName().encode()) +
                    hash(self.dependencyNode.uuid().asString())
            )

        return self._HASH

    def __repr__(self) -> str:

        """
        The representation of the node as a string

        :return: str, the representation of the node
        """

        return f'{self.__class__.__name__}("{self.name}")'

    def __str__(self) -> str:

        """
        The name of the node

        :return: str, then name of the node
        """

        return self.name

    # TODO: implement __getattr__ (ie: Node().attributeName)
    # def __getattr__(self, attr: str) -> Callable:
    #     print(f'{self.__class__.__name__}.__getattr__({attr=})')
    #
    #     if hasattr(self.__dependencyNode, attr):
    #         def wrapOutput(*args, **kwargs):
    #             result = getattr(self.__dependencyNode, attr)(*args, **kwargs)
    #             if isinstance(result, om.MPlug):
    #                 return Plug(result)
    #
    #             return result
    #
    #         return wrapOutput
    #
    #     # Raise the native python error if nothing was found
    #     return super().__getattr__(attr)

    def get(self, plug, defaultValue: Any = None) -> Union[Plug, Any]:
        """
        Safe __getitem__, retrieve a plug from the current node

        :param plug: Plug, the plug to retrieve
        :param defaultValue: Any, the default value to return if the plug is not found

        :return:Union[Plug, Any], the plug or an empty Plug or the defaultValue

        """
        if self.hasAttr(plug):
            return self[plug]

        return Plug() if defaultValue is None else defaultValue

    def __getitem__(self, plug: Union[str, Plug]) -> Plug:
        """
        Convenient implementations to retrieve a plug from the current node

        :param plug: Plug, the plug to retrieve

        :return: Plug, the wanted plug
        """
        attr = self.dependencyNode.findAlias(plug)
        if not attr.isNull():
            plg = Plug(self, attr)

            if plug == plg.partialName(includeNodeName=False, useAlias=True):
                return plg

            elif plg.isArray:
                for idx in range(plg.numElements()):
                    child = plg.elementByLogicalIndex(idx)
                    if child.partialName(includeNodeName=False, useAlias=True) == plug:
                        return child

        try:
            return Plug(self.dependencyNode.findPlug(plug, True))

        except Exception:
            raise CmdoPlugException(
                f'{self}.__getitem__({plug}) -> {self}.{plug} not found'
            )

    def __setitem__(self, plug, value) -> None:
        """
        Convenient implementations to set a plug on the current node

        """

        if isinstance(value, tuple):
            self[plug].set(*value)

        else:
            self[plug].set(value)

    def printClass(self) -> None:
        """
        Get a representation the class and all its members

        :return: str, string representation of the current class
        """

        text = "\n"
        text += "\n# ######################################"
        text += f"\n# - {self.__class__.__name__.upper()} MEMBERS:"
        text += "\n# ######################################"

        for name, value in self.getData().items():
            text += f'\n\n\t- {str(name):<20}: {value}'

        print(text)

    def getData(self) -> Dict:
        """
        Data representing the class and its members

        :return: dict: class members except excluded names and patterns
        """
        data = {}
        excluded_types, excluded_names = self.getExcludedMembers()

        for name in dir(self.__class__):
            try:
                value = getattr(self, name)
            except Exception:
                continue

            obj_type = type(value)

            if any(dnpt in str(obj_type) for dnpt in excluded_types):
                continue

            if any(dnpn == name for dnpn in excluded_names):
                continue

            data[name] = value

        return data

    def setAttrFromDict(self, data: Dict[str, Any]) -> None:
        """
        Set multiple attributes from given dictionary

        :param data: dict[str, Any], a dictionary of {attrName: attrValue} pairs
        """

        for attr, value in data.items():

            self[attr] = value

    def getAttrFromList(self, data: List[str]) -> Dict[str, Any]:
        """
        Get multiple attribute values from a list of attribute names

        :param data: list[str], a list of attribute names to get values for

        :return: dict[str, Any], a dictionary of {attrName: attrValue} pairs
        """

        return {
            attrName: self[attrName].value
            for attrName in data
        }

    @property
    def dependencyNode(self) -> om.MFnDependencyNode:
        """
        Get a copy of the current object s dependencyNode

        :return: om.MFnDependencyNode, the dependency node
        """

        return self.__dependencyNode

    @property
    def hash(self) -> int:
        """
        Get the current instance hash

        :return: int, the hash value
        """

        return hash(self)

    @property
    def name(self) -> str:
        """
        Get the name or partialName of the current node

        :return: str, the name of the node
        """

        if self.__dependencyNode.hasUniqueName():
            return self.__dependencyNode.name()

        return om.MFnDagNode(self).partialPathName()

    @name.setter
    def name(self, value: str) -> None:
        """
        Set the name of the current node

        :param value: str, the name to give to the current node
        """

        self.__dependencyNode.setName(value)

    @property
    def strippedName(self) -> Optional[str]:

        """
        Get the name without namespace

        :return: Optional[str], the name without namespace
        """

        return om.MNamespace.stripNamespaceFromName(self.name)

    @strippedName.setter
    def strippedName(self, name: str) -> None:

        """
        Set the name without namespace

        :param name: str, The new name without namespace

        """

        self.name = (
            name
            if self.namespace is None
            else f"{self.namespace}:{name}"
        )

    @property
    def namespace(self) -> Optional[str]:

        """
        Get the namespace of the current node

        :return: str, the namespace of the node
        """

        return om.MNamespace.getNamespaceFromName(self.name)

    @namespace.setter
    def namespace(self, namespace: Union[str, None]) -> None:

        """
        Set the current node s namespace

        :param namespace: Union[str, None], the namespace of the node
        """

        stripped_name = om.MNamespace.stripNamespaceFromName(self.name)

        if namespace is not None and not om.MNamespace.namespaceExists(namespace):
            om.MNamespace.addNamespace(namespace)

        self.name = f"{namespace}:{stripped_name}" if namespace else stripped_name

    @property
    def type(self) -> str:
        """
        Returns the maya type of the current Node

        :return: str, the maya type of the current node
        """
        return cmds.nodeType(self.name)

    @property
    def mayaObjectHandle(self) -> om.MObjectHandle:

        """
        Get the MObjectHandle of the current node
        MObjectHandle if a MObject wrapper that makes it easy to verify
        if the object is valid

        :return: om.MObjectHandle, the MObjectHandle of the node
        """

        return om.MObjectHandle(self)

    @property
    def isValidDependencyNode(self) -> bool:
        """
        Is MFnDependencyNode valid

        :return: bool, Is MFnDependencyNode valid
        """

        return self.dependencyNode.hasObj(self)

    def hasAttr(self, attr: Union[str, Plug]) -> bool:
        """
        Check if the current node has the given attribute

        :param attr: Union[str, Plug], the name of the attribute or the Plug
        :return: bool, if the current node has the given attribute
        """

        if isinstance(attr, Plug):
            attr = attr.name()

        return self.dependencyNode.hasAttribute(attr)

    def addAttr(self, *args, **kwargs) -> Plug:
        """
        Re-implementation of cmds.addAttr

        :param kwargs: Dict[str, Any], a dict of {attrName: attrValue} pairs

        :return: Plug, the newly created attribute plug
        """

        attrName = (
            args[0] if args else
            kwargs.get("longName") or kwargs.get("ln") or
            kwargs.get("shortName") or kwargs.get("sn")
        )

        cmds.addAttr(self.name, **kwargs)

        # we need to do this because of compounds attributes
        return self[attrName] if self.hasAttr(attrName) else None

    # TODO: implement delete attribute function
    def deleteAttr(self, attribute: Union[str, Plug]) -> None:
        """
        Re-implementation of cmds.deleteAttr

        :param attribute: Union[str, Plug], the attribute to delete

        """

        if not self.hasAttr(attribute):
            return

        mPlugObj = self[attribute].attribute()
        self.dependencyNode.removeAttribute(mPlugObj)

    @property
    def connectedPlugs(self) -> PlugArray:
        """
        Get all connected plugs from the current node

        :return: PlugArray, an array of connected plugs
        """

        return PlugArray(self.dependencyNode.getConnections())

    @property
    def isConnected(self) -> bool:
        """
        If the current node has connections, incoming and/or outgoing

        :return: bool, if the current node has connections
        """

        return bool(self.connectedPlugs)

    @property
    def incomingConnections(self) -> Dict[Plug, Plug]:

        """
        Get a dictionary holding incoming connections

        ie: dict(currentNodePlug: connectedPlug)

        :return: dict[Plug, Plug], the incoming connections
        """

        connection_dict = {}

        for plug in self.connectedPlugs:
            if not plug.isDestination:
                continue

            connection_dict[plug] = plug.source()

        return connection_dict

    @property
    def outgoingConnections(self) -> Dict[Plug, Plug]:

        """
        Get a dictionary holding outgoing connections

        ie: dict(currentNodePlug: connectedPlug)

        :return: dict[Plug, Plug], the outgoing connections
        """

        connection_dict = {}

        for plug in self.connectedPlugs:
            if not plug.isSource:
                continue

            connection_dict[plug] = plug.destinations()

        return connection_dict

    @property
    def isMayaObjectValid(self) -> bool:

        """
        Get the node validity state from the object handle

        :return: bool, if the current node is valid
        """

        return self.mayaObjectHandle.isValid()

    @property
    def isDagNode(self) -> bool:

        """
        Is the current node a MFnDagNode

        :return: bool, Is the current node a MFnDagNode
        """

        return self.hasFn(om.MFn.kDagNode)

    @property
    def isShapeNode(self) -> bool:

        """
        Is the current node a MFnDagNode of type KShape

        :return: bool, Is the current node a MFnDagNode of type KShape
        """

        return self.hasFn(om.MFn.kShape)

    @property
    def exists(self) -> bool:

        """
        Does the object exist

        :return: bool, the inverse null state of the object
        """

        return not self.isNull()

    @property
    def isReferenced(self) -> bool:
        """
        Check if the current node is referenced

        :return: bool, Is the current node is referenced
        """

        return self.dependencyNode.isFromReferencedFile

    @property
    def referenceNode(self) -> Union[om.MObject, None]:
        """
        The reference node of the current node or None

        :return: Union[om.MObject, None], the reference node or None
        """

        if not self.isReferenced:
            return None

        from ..nodeRegistry import NodeRegistry

        refNodeName = cmds.referenceQuery(self.name, referenceNode=True)
        refNode = om.MSelectionList().add(refNodeName).getDependNode(0)

        return NodeRegistry().get(refNodeName)(refNode)


NodeType = Type[Union[str, Node]]
