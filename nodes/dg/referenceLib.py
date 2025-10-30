from typing import Optional, List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry
from ...core.graphLib import Graph


# TODO: continue updating class with more properties/functions
class Reference(dgLib.DGNode):

    _NODE_TYPE = "reference"
    _API_TYPE = om.MFn.kReference

    @property
    def mfnReference(self) -> om.MFnReference:
        """
        Get MFnReference of the om.MObject

        :return: om.MFnReference, the Reference object
        """

        return om.MFnReference(self)

    @property
    def filePath(self) -> str:
        """
        Get the referenced file path

        :return: str, the referenced file path
        """

        return self.mfnReference.fileName(True, False, False)

    @property
    def namespace(self) -> str:
        """
        Get the namespace associated with this reference

        :return: str, the namespace associated with this reference
        """

        return self.mfnReference.associatedNamespace(True)

    @property
    def isValid(self) -> bool:
        """
        Check if the reference is valid

        :return: bool, is the reference valid
        """

        return self.mfnReference.isValidReference()

    @property
    def isLoaded(self) -> bool:
        """
        Check if the reference is loaded

        :return: bool, is the reference loaded
        """

        return self.mfnReference.isLoaded()

    @property
    def isLocked(self):
        """
        Check if the reference is locked

        :return: bool, is the reference locked
        """

        return self.mfnReference.isLocked()

    @property
    def nodes(self) -> Graph:
        """
        Retrieve the referenced nodes

        :return: Graph, a list of referenced nodes
        """

        return Graph.ls(*self.mfnReference.nodes())

    def containsNode(self, node: om.MObject) -> bool:
        """
        Check if the node is contained in this reference
         and its children references

        :param node: om.MObject, the node to check

        :return: bool, is the node contained in this reference
        """

        return self.mfnReference.containsNode(node)

    def containsNodeExactly(self, node: om.MObject) -> bool:
        """
        Check if the node is contained in this reference
         without its children references

        :param node: om.MObject, the node to check

        :return: bool, is the node contained in this reference
        """

        return self.mfnReference.containsNodeExactly(node)


NodeRegistry()[Reference.nodeType()] = Reference
