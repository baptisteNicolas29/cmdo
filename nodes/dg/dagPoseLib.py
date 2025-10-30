from typing import Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.plugsLib import PlugArray
from ...core.nodeRegistry import NodeRegistry


class DagPose(dgLib.DGNode):

    _NODE_TYPE = "dagPose"
    _API_TYPE = om.MFn.kDagPose

    @property
    def bindPose(self) -> bool:
        """
        Get the bindPose value

        :return: bool, the bindPose value
        """
        return self['bindPose'].asBool()

    @property
    def globalMode(self) -> bool:
        """
        Get the global value

        :return: bool, the global value
        """
        return self['global'].asBool()

    @property
    def memberCount(self) -> int:
        """
        Get the number of members

        :return: int, the number of members
        """
        return self['members'].numElements()

    @property
    def parentCount(self) -> int:
        """
        Get the number of parents

        :return: int, the number of parents
        """
        return self['parents'].numElements()

    @property
    def worldMatrixCount(self) -> int:
        """
        Get the number of worldMatrices

        :return: int, the number of worldMatrices
        """
        return self['worldMatrix'].numElements()

    @property
    def members(self) -> om.MPlugArray:
        """
        Get a plugArray of all members

        :return: om.MPlugArray, a plugArray of all members
        """
        memberArray = PlugArray()

        for i in range(self['members'].numElements()):
            memberArray.append(self['members'][i])

        return memberArray

    @property
    def parents(self) -> om.MPlugArray:
        """
        Get a plugArray of all parents

        :return: om.MPlugArray, a plugArray of all parents
        """
        parentArray = PlugArray()

        for i in range(self['parents'].numElements()):
            parentArray.append(self['parents'][i])

        return parentArray

    @property
    def worldMatrices(self) -> om.MPlugArray:
        """
        Get a plugArray of all worldMatrices

        :return: om.MPlugArray, a plugArray of all worldMatrices
        """
        worldMatrixArray = PlugArray()

        for i in range(self['worldMatrix'].numElements()):
            worldMatrixArray.append(self['worldMatrix'][i])

        return worldMatrixArray

    @property
    def world(self) -> om.MPlugArray:
        """
        Get a plugArray of all world

        :return: om.MPlugArray, a plugArray of all world
        """
        worldArray = PlugArray()

        for plug in self['world'].destinations():
            worldArray.append(plug)

        return worldArray

    @property
    def skinClusters(self) -> om.MSelectionList:
        """
        Get an om.MSelectionList of all connected skinClusters

        :return: om.MSelectionList, a MSelectionList of all skinCluster nodes
        """
        skinclusterList = om.MSelectionList()

        for plug in self['message'].destinations():
            skinclusterList.add(plug.node())

        return skinclusterList

    def getMember(self, value: int) -> om.MPlug:
        """
        Get a specific member
        
        :param value: int, the index of the member to get
        
        :return: om.MPlug, the connected member plug
        """
        
        return self['members'][value].source()

    def getParent(self, value: int) -> om.MPlug:
        """
        Get a specific parent

        :param value: int, the index of the parent to get

        :return: om.MPlug, the connected parent plug
        """

        return self['parents'][value].source()

    def getWorldMatrix(self, value: int) -> om.MPlug:
        """
        Get a specific worldMatrix

        :param value: int, the index of the worldMatrix to get

        :return: om.MPlug, worldMatrix value
        """

        return self['worldMatrix'][value].value


NodeRegistry()[DagPose.nodeType()] = DagPose
