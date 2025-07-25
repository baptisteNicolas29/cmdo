from typing import Optional, Union

from maya import cmds as mc
from maya.api import OpenMaya as om

from ...core.nodeRegistry import NodeRegistry
from ...core.abstract import dagLib


class Mesh(dagLib.DAGNode):

    _NODE_TYPE = "mesh"
    _API_TYPE = om.MFn.kMesh

    def __init__(self, name: Union[str, om.MObject] = None) -> None:

        """
        Initialize an instance of Mesh

        Args:
            name: Optional[str], the name of the node
        """

        super().__init__(name=name)

        # self._init_mesh_properties()

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

        return om.MItMeshVertex(self)

    @property
    def numVertices(self) -> Optional[int]:

        """
        Get the vertex count

        Returns:
            int: the number of vertices
        """

        return self.mfnMesh.numVertices

    @property
    def numEdges(self) -> Optional[int]:

        """
        Get the edge count

        Returns:
            int: the number of edges
        """

        return self.mfnMesh.numEdges

    @property
    def numFaces(self) -> Optional[int]:

        """
        Get the face count

        Returns:
            int: the number of faces
        """

        return self.mfnMesh.numPolygons

    @property
    def invisibleFaces(self) -> Optional[om.MUintArray]:

        """
        Get the mesh invisible faces

        Returns
            om.MUintArray: the mesh invisible faces
        """

        return self.mfnMesh.getInvisibleFaces()

    @property
    def numInvisibleFaces(self) -> int:

        """
        Retourne le nombre de faces invisibles du maillage.

        Returns
            om.MUintArray
                Les faces invisibles du maillage.
        """

        return len(self.invisibleFaces)

    @property
    def points(self) -> Optional[om.MPointArray]:

        """
        Get vertice positions in object space

        Returns
            om.MPointArray: the vertex positions
        """

        return self.mfnMesh.getPoints(space=om.MSpace.kObject)

    @property
    def numUVSets(self) -> Optional[int]:

        """
        Get the number of UV sets

        Returns
            int: the number of UV sets
        """

        return self.mfnMesh.numUVSets

    @property
    def currentUVSet(self) -> Optional[str]:

        """
        Get the current UV set

        Returns
            str: the current UV set
        """

        return self.mfnMesh.currentUVSetName()

    @property
    def numColorSets(self) -> Optional[int]:

        """
        Get the number of color sets

        Returns
            int: the number of color sets
        """

        return self.mfnMesh.numColorSets

    @property
    def currentColorSet(self) -> Optional[str]:

        """
        Get the current Color set

        Returns
            str: the current Color set
        """

        return self.mfnMesh.currentColorSetName()

    @property
    def displayColors(self) -> bool:

        """
        Are colors displayed on the mesh node

        Returns
            bool:
        """

        return self.mfnMesh.displayColors

    # @staticmethod
    # def check_point_have_transform(self):
    #
    #     indices = []
    #
    #     if not self.shape_orig.exists:
    #         return False
    #
    #     mfn_mesh = self.mesh_fn
    #     mfn_orig = self.shape_orig.mesh_fn
    #
    #     mesh_points = mfn_mesh.getPoints(om.MSpace.kObject)
    #     orig_points = mfn_orig.getPoints(om.MSpace.kObject)
    #
    #     for i in range(len(mesh_points)):
    #         if not mesh_points[i].isEquivalent(orig_points[i]):
    #             indices.append(i)
    #
    #     return True, indices

# -- Mesh Properties ----------------------------------------------------------
# -----------------------------------------------------------------------------
    @property
    def checkSamePointTwice(self) -> bool:

        """
        Check if created or added points don t exist twice on the same mesh

        Returns
            bool
                True si les polygones créés ou ajoutés au node de Mesh
                ne contiennent pas deux fois le même point.
                False sinon.
        """

        return self.mfnMesh.checkSamePointTwice

    @property
    def intermediateObject(self) -> bool:

        """
        Get the intermediateObject value

        Returns:
            bool: the intermediateObject value
        """

        return self['intermediateObject'].asBool()

    @intermediateObject.setter
    def intermediateObject(self, value: Union[bool, int]) -> None:
        """
        Set the intermediateObject value

        Args:
            value: Union[bool, int], the intermediateObject value
        """

        self['intermediateObject'] = value


NodeRegistry()[Mesh.nodeType()] = Mesh
