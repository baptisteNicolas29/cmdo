from typing import Union

from maya.api import OpenMaya as om

from ...core.abstract import dg_lib
from ...core.plugs_lib import PlugArray
from ...core.node_registry import NodeRegistry


class DagPose(dg_lib.DGNode):

    _NODE_TYPE = "dagPose"
    _API_TYPE = om.MFn.kDagPose

    def __init__(self, name: Union[str, om.MObject] = None) -> None:

        """
        Initialize an instance of DagPose

        Args:
            name: str | om.MObject, the name of the node
        """

        super().__init__(name=name)

    @property
    def bindPose(self) -> bool:
        """
        Get the bindPose value

        Returns:
            bool, the bindPose value
        """
        return self['bindPose'].asBool()

    @property
    def globalMode(self) -> bool:
        """
        Get the global value

        Returns:
            bool, the global value
        """
        return self['global'].asBool()

    @property
    def memberCount(self) -> int:
        """
        Get the number of members

        Returns:
            int: the number of members
        """
        return self['members'].numElements()

    @property
    def parentCount(self) -> int:
        """
        Get the number of parents

        Returns:
            int: the number of parents
        """
        return self['parents'].numElements()

    @property
    def worldMatrixCount(self) -> int:
        """
        Get the number of worldMatrices

        Returns:
            int: the number of worldMatrices
        """
        return self['worldMatrix'].numElements()

    @property
    def members(self) -> om.MPlugArray:
        """
        Get a plugArray of all members

        Returns:
            om.MPlugArray, a plugArray of all members
        """
        memberArray = PlugArray()

        for i in range(self['members'].numElements()):
            memberArray.append(self['members'][i])

        return memberArray

    @property
    def parents(self) -> om.MPlugArray:
        """
        Get a plugArray of all parents

        Returns:
            om.MPlugArray, a plugArray of all parents
        """
        parentArray = PlugArray()

        for i in range(self['parents'].numElements()):
            parentArray.append(self['parents'][i])

        return parentArray

    @property
    def worldMatrices(self) -> om.MPlugArray:
        """
        Get a plugArray of all worldMatrices

        Returns:
            om.MPlugArray, a plugArray of all worldMatrices
        """
        worldMatrixArray = PlugArray()

        for i in range(self['worldMatrix'].numElements()):
            worldMatrixArray.append(self['worldMatrix'][i])

        return worldMatrixArray

    @property
    def world(self) -> om.MPlugArray:
        """
        Get a plugArray of all world

        Returns:
            om.MPlugArray, a plugArray of all world
        """
        worldArray = PlugArray()

        for plug in self['world'].destinations():
            worldArray.append(plug)

        return worldArray

    @property
    def skinClusters(self) -> om.MSelectionList:
        """
        Get an om.MSelectionList of all connected skinClusters

        Returns:
            om.MSelectionList, a MSelectionList of all skinCluster nodes
        """
        skinclusterList = om.MSelectionList()

        for plug in self['message'].destinations():
            skinclusterList.add(plug.node())

        return skinclusterList

    def getMember(self, value: int) -> om.MPlug:
        """
        Get a specific member
        
        Args:
            value: int, the index of the member to get
        
        Returns:
            om.MPlug, the connected member plug
        """
        
        return self['members'][value].source()

    def getParent(self, value: int) -> om.MPlug:
        """
        Get a specific parent

        Args:
            value: int, the index of the parent to get

        Returns:
            om.MPlug, the connected parent plug
        """

        return self['parents'][value].source()

    def getWorldMatrix(self, value: int) -> om.MPlug:
        """
        Get a specific worldMatrix

        Args:
            value: int, the index of the worldMatrix to get

        Returns:
            om.MPlug, worldMatrix value
        """

        return self['worldMatrix'][value].value


NodeRegistry()[DagPose.nodeType()] = DagPose
