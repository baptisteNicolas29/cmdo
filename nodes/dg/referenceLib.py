from typing import Optional, List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry
from ...core.graphLib import Graph


# TODO: continue updating class with more properties/functions
class Reference(dgLib.DGNode):

    _NODE_TYPE = "reference"
    _API_TYPE = om.MFn.kReference

    def __init__(self, name: Union[str, om.MObject] = None) -> None:

        """
        Initialize an instance of Absolute

        Args:
            name: str | om.MObject, the name of the node
        """

        super().__init__(name=name)

    @property
    def mfnReference(self) -> om.MFnReference:
        """
        Get mfnReference of the om.MObject

        Returns:
            om.mfnReference: the skinCluster object
        """
        return om.MFnReference(self)

    @property
    def filePath(self) -> str:

        return self.mfnReference.fileName(True, False, False)

    @property
    def namespace(self) -> str:

        return self.mfnReference.associatedNamespace(True)

    @property
    def nodes(self):
        graph = Graph()
        for obj in self.mfnReference.nodes():
            graph.add(obj)

        return graph


NodeRegistry()[Reference.nodeType()] = Reference
