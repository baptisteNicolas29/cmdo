from typing import Optional, Union, List, Set, Type

from maya.api import OpenMaya as om, OpenMayaAnim as oma

from . import dgLib
from ...core import graphLib


class GeometryFilter(dgLib.DGNode):

    def __init__(self, name: Union[str, om.MObject] = None) -> None:
        """
        Initialize an instance of GeometryFilter

        :param name: Optional[str], the name of the node
        """

        super().__init__(name=name)

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
