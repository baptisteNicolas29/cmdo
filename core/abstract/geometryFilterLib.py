from typing import Optional, Union, List, Set, Type

from maya.api import OpenMaya as om, OpenMayaAnim as oma

from . import dgLib
from ...core import graphLib


class GeometryFilter(dgLib.DGNode):

    @property
    def mfnGeometryFilter(self) -> oma.MFnGeometryFilter:
        """
        Get mfnGeometryFilter of the om.MObject

        :return: oma.MFnGeometryFilter, the geometryFilter object
        """

        return oma.MFnGeometryFilter(self)

    @property
    def envelope(self) -> float:
        """
        Get the envelope value of the current deformer

        :return: float, the value of the envelope
        """

        return self.mfnGeometryFilter.envelope

    @envelope.setter
    def envelope(self, value: float) -> None:
        """
        Get the envelope value of the current deformer

        :param value: float, the value of the envelope
        """

        self.mfnGeometryFilter.envelope = float(value)

    @property
    def deformerSet(self):
        """
        Get the envelope value of the current deformer

        :return: float, the value of the envelope
        """

        return self.mfnGeometryFilter.deformerSet

    @property
    def inputGeometry(self) -> graphLib.Graph:

        graph = graphLib.Graph()
        mObjectArray = self.mfnGeometryFilter.getInputGeometry()

        for mObject in mObjectArray:
            graph.add(mObject)

        return graph

    @property
    def outputGeometry(self) -> graphLib.Graph:

        graph = graphLib.Graph()
        mObjectArray = self.mfnGeometryFilter.getOutputGeometry()

        for mObject in mObjectArray:
            graph.add(mObject)

        return graph

    @property
    def weightList(self) -> List[List[float]]:
        weightLists = []
        for weightList in self['weightList']:
            plug = weightList['weights']

            ids = plug.getExistingArrayAttributeIndices()
            count = len(ids)

            weights = [0.0] * count

            for i in range(count):
                weights[i] = plug.elementByPhysicalIndex(i).asFloat()

            weightLists.append(weights)

        return weightLists

    @weightList.setter
    def weightList(self, weights: List[List[float]]) -> None:
        for weightList in self['weightList']:
            plug = weightList['weights']

            ids = plug.getExistingArrayAttributeIndices()
            count = len(ids)

            for i in range(count):
                plug.elementByLogicalIndex(ids[i]).setFloat(weights[i])
