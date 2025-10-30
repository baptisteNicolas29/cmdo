from typing import Optional, Union

from maya import cmds
from maya.api import OpenMaya as om

from ...core.nodeRegistry import NodeRegistry
from ...core.abstract import dagLib


class Mesh(dagLib.DAGNode):

    _NODE_TYPE = "mesh"
    _API_TYPE = om.MFn.kMesh

    @property
    def mfnMesh(self) -> om.MFnMesh:

        """
        Get MFnMesh of the om.MObject

        Returns:
            om.MFnMesh: the mesh object
        """

        return om.MFnMesh(self)

    @property
    def mitMeshVertex(self) -> om.MItMeshVertex:
        """
        Get a mesh vertex iterator

        :return: om.MItMeshVertex: the mesh vertex iterator
        """
        return om.MItMeshVertex(self)

    @property
    def numVertices(self) -> Optional[int]:

        """
        Get the vertex count

        :return: int, the number of vertices
        """

        return self.mfnMesh.numVertices

    @property
    def numEdges(self) -> Optional[int]:

        """
        Get the edge count

        :return: int, the number of edges
        """

        return self.mfnMesh.numEdges

    @property
    def numFaces(self) -> Optional[int]:

        """
        Get the face count

        :return: int, the number of faces
        """

        return self.mfnMesh.numPolygons

    @property
    def invisibleFaces(self) -> Optional[om.MUintArray]:

        """
        Get the mesh invisible faces

        :return: om.MUintArray, the mesh invisible faces
        """

        return self.mfnMesh.getInvisibleFaces()

    @property
    def numInvisibleFaces(self) -> int:

        """
        Get the number of invisible faces

        :return: om.MUintArray, the number of invisible faces
        """

        return len(self.invisibleFaces)

    @property
    def points(self) -> Optional[om.MPointArray]:

        """
        Get vertice positions in object space

        :return om.MPointArray: the vertex positions
        """

        return self.mfnMesh.getPoints(space=om.MSpace.kObject)

    @property
    def numUVSets(self) -> Optional[int]:

        """
        Get the number of UV sets

        :return: int, the number of UV sets
        """

        return self.mfnMesh.numUVSets

    @property
    def currentUVSet(self) -> Optional[str]:

        """
        Get the current UV set

        :return: str, the current UV set
        """

        return self.mfnMesh.currentUVSetName()

    @property
    def numColorSets(self) -> Optional[int]:

        """
        Get the number of color sets

        :return: int, the number of color sets
        """

        return self.mfnMesh.numColorSets

    @property
    def currentColorSet(self) -> Optional[str]:

        """
        Get the current Color set

        :return: str, the current Color set
        """

        return self.mfnMesh.currentColorSetName()

    @property
    def displayColors(self) -> bool:

        """
        Are colors displayed on the mesh node

        :return: bool, are the colors displayed on this mesh node
        """

        return self.mfnMesh.displayColors

    def checkDifferenceWithOrigShape(self):
        """

        :return:
        """

        indices = []
        mesh = self.parents[0]

        shape_deform = [
            shape
            for shape in mesh.shapes
            if not shape.intermediateObject
        ]
        shape_orig = [
            shape
            for shape in mesh.shapes
            if shape.intermediateObject
        ]

        if not shape_orig:
            return []

        mfn_mesh = shape_deform[0].mfnMesh
        mfn_orig = shape_orig[0].mfnMesh

        mesh_points = mfn_mesh.getPoints(space=om.MSpace.kObject)
        orig_points = mfn_orig.getPoints(space=om.MSpace.kObject)

        for i in range(len(mesh_points)):
            if mesh_points[i].isEquivalent(orig_points[i], tol=0.0001):
                continue

            indices.append(i)

        return indices

    @property
    def checkSamePointTwice(self) -> bool:

        """
        Check if created or added points exist twice on the same mesh

        :return: bool, if the created or added points exist twice on the same mesh
        """

        return self.mfnMesh.checkSamePointTwice

    @property
    def intermediateObject(self) -> bool:

        """
        Get the intermediateObject value

        :return: bool, the intermediateObject value
        """

        return self['intermediateObject'].asBool()

    @intermediateObject.setter
    def intermediateObject(self, value: Union[bool, int]) -> None:
        """
        Set the intermediateObject value

        :param value: Union[bool, int], the intermediateObject value
        """

        self['intermediateObject'] = value


NodeRegistry()[Mesh.nodeType()] = Mesh
