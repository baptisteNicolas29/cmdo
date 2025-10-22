from typing import Optional, List, Type, Union

from maya import cmds
from maya.api import OpenMaya as om

from ..plugsLib import Plug
from .dgLib import DGNode
from ..nodeRegistry import NodeRegistry


class DAGNode(DGNode):

    def __init__(self, name: Union[str, om.MObject] = None) -> None:

        """
        Initialize an instance of DAGNode

        Args:
            name: str, the name of the node
        """

        super().__init__(name=name)

    def __str__(self) -> str:
        return self.name

    @property
    def dagPath(self) -> om.MDagPath:

        """
        Get the node s MDagPath.

        MDagPath is used to access nodes in the Directed Acyclic Graph (DAG).
        This corresponds mainly to nodes visible in the outliner such as
        transforms, geometries, lights, cameras ect

        MFnDagNode.dagPath() method, does not work
         because we initialize our MFnDagNode with an MObject

        Returns:
            Optional[MDagPath]: the node s MDagPath
        """

        return self.mfnDagNode.getAllPaths()[0]

    @property
    def isDagPathValid(self) -> bool:

        """
        Is MFnDagPath valid

        Returns:
            bool: if the MFnDagPath is valid or not
        """

        return self.dagPath.isValid()

    @property
    def fullName(self) -> str:

        """
        The full name including parents of the current node

        Returns:
            str: the full name of the current node
        """

        return self.dagPath.fullPathName()

    @property
    def shortName(self) -> str:

        """
        The smallest unique name for the current node

        Returns:
            str: the short name of the current node
        """

        return self.dagPath.partialPathName()

    @property
    def mfnDagNode(self) -> om.MFnDagNode:

        """
        Get the node s MFnDagNode

        Returns:
            Optional[MFnDagNode]: the MFnDagNode of the current node
        """

        return om.MFnDagNode(self)

    @property
    def isDagNodeValid(self) -> bool:

        """
        Is MFnDagNode valid

        Returns:
            bool: if the MFnDagNode is valid or not
        """

        return self.mfnDagNode.hasObj(self)

    @property
    def childCount(self) -> int:

        """
        The number of children of the current node

        Returns:
            int: The number of children of the current node
        """

        return self.dagPath.childCount()

    @property
    def children(self) -> list:

        """
        Get hierarchical children of the current node

        Returns:
            list[DAGNode]: the list of children objects
        """
        items = []
        for idx in range(self.mfnDagNode.childCount()):
            child_obj = self.mfnDagNode.child(idx)

            items.append(NodeRegistry().get(child_obj, DAGNode)(child_obj))

        return items

    @property
    def childNames(self) -> List[str]:

        """
        Get hierarchical children names of the current node

        Returns:
            List[str]: the list of children names if any
        """

        return [child.name for child in self.children]

    @property
    def shapeCount(self) -> int:

        """
        The number of shapes the current transform has

        Returns:
            int: The number of shapes the current transform has
        """

        return self.dagPath.numberOfShapesDirectlyBelow()

    @property
    def shapes(self) -> List[str]:

        """
        The shapes held by the current node

        Returns:
            List[str]: the shape names of None
        """

        return [child for child in self.children if child.isShape]

    @property
    def shapeOrig(self) -> Optional[Type["DAGNode"]]:

        """
        Return the node s original shape
        OrigShapes are shapes saved by maya to remember the initial state of
        a mesh before deformations

        Returns:
            Optional[Type["DAGNode"]]: the shape orig or None
        """

        return NotImplementedError('"shapeOrig" property is not implemented yet')

    @property
    def isOrig(self) -> bool:

        """
        Is this the original shape (shapeOrig)

        Returns:
            bool: if the shape is the shapeOrig or not
        """

        return NotImplementedError('"isOrig" property is not implemented yet')

    @property
    def parents(self) -> List:
        """
        Get the parent nodes of the current node

        Returns:
             list[DAGNode]: The parents of the current node
        """
        items = []
        for idx in range(self.mfnDagNode.parentCount()):
            parentObj = self.mfnDagNode.parent(idx)
            parentName = om.MFnDagNode(parentObj).partialPathName()

            if parentObj.apiType() == om.MFn.kWorld:
                return []

            items.append(NodeRegistry().get(parentName, DAGNode)(parentObj))

        return items

    @parents.setter
    def parents(self, parent: Type["DAGNode"] = None) -> None:

        """
        Sets the current node s new parent.

        If None is supplied, parents the
        current node to the scene root node (aka: parent to world)

        Args:
            parent: str, the name of the new parent, if None, parents to root

        """

        if isinstance(parent, str):
            parent = DAGNode(parent)

        elif parent is None:
            parent = om.MObject.kNullObj

        om.MDagModifier().reparentNode(self, parent).doIt()

    @property
    def dagRoot(self) -> 'DAGNode':

        """
        Get the root parent node of the current node or self if it is the root

        Returns:
             DAGNode: The root parent of the current node
        """

        parentNodePath = self.dagPath.pop(self.dagPath.length()-1)

        if parentNodePath == self.dagPath:
            return self

        mObj = parentNodePath.node()
        return NodeRegistry().get(mObj, DAGNode)(mObj)
        
    @property
    def isTransform(self) -> bool:

        """
        Is current node a transform

        Returns:
            bool: is node a transform
        """
        return self.dagPath.hasFn(om.MFn.kTransform)

    @property
    def isShape(self) -> bool:

        """
        Is current node a shape

        Returns:
            bool: is node a shape
        """
        return not self.isTransform and self.dagPath.hasFn(om.MFn.kShape)

    @property
    def drawOverrideInfo(self) -> om.MDAGDrawOverrideInfo:

        """
        Get the draw override info for the current node

        Returns:
            om.MDrawOverrideInfo: the draw info object
        """

        return self.dagPath.getDrawOverrideInfo()

    @property
    def overrideEnabled(self) -> bool:

        """
        Is draw override info enabled

        Returns:
            bool: Is draw override info  enabled
        """

        return self.drawOverrideInfo.overrideEnabled

    @overrideEnabled.setter
    def overrideEnabled(self, value: bool) -> None:

        """
        Enable or Disable the drawOverride state

        Args:
            value: bool, state of the drawOverride

        """

        self["overrideEnabled"] = value

    @property
    def overrideRGBColors(self) -> int:

        """
        The index of the RGB color for the draw override

        Returns:
            int: the index of the RGB color
        """

        return self['overrideRGBColors'].asInt()

    @overrideRGBColors.setter
    def overrideRGBColors(self, value: int) -> None:

        """
        Set the RBG color index for the draw override

        Args:
            value: int, the index of the RGB color to use

        """

        self["overrideRGBColors"] = value

    @property
    def rgbColor(self) -> List[float]:

        """
        The RGB color vector from the draw override

        Returns:
            List[float]: the RGB vector3
        """

        return [
            self["overrideColorR"].asFloat(),
            self["overrideColorG"].asFloat(),
            self["overrideColorB"].asFloat()
        ]

    @rgbColor.setter
    def rgbColor(self, value: List[float]) -> None:

        """
        Set the draw override RGB colors

        Args:
            value: List[float], RGB color vector3

        """

        self["overrideColorR"] = value[0]
        self["overrideColorG"] = value[1]
        self["overrideColorB"] = value[2]

    @property
    def overrideColor(self) -> Optional[int]:

        """
        The index of the color for the draw override

        Returns:
            int: the index of the current draw override color
        """

        return self['overrideColor'].asInt()

    @overrideColor.setter
    def overrideColor(self, value: int) -> None:

        """
        Set the index for the draw override color

        Args:
            value: int, the index of the color to set

        """

        self["overrideColor"] = value

    @property
    def boundingBox(self) -> om.MBoundingBox:

        """
        The bounding box of the current node

        Returns:
            om.MBoundingBox: the bounding box of the current node
        """

        return self.mfnDagNode.boundingBox

    @property
    def transformationMatrix(self) -> om.MMatrix:

        """
        Get the local transformation matrix of the current node

        Returns:
            om.MMatrix: the transformation matrix
        """

        return self.mfnDagNode.transformationMatrix()

    @transformationMatrix.setter
    def transformationMatrix(self, matrix: om.MMatrix) -> None:

        """
        Set the local transformation matrix of the current node

        Args:
            matrix: om.MMatrix, The transformation matrix of the current node

        """

        om.MFnTransform(self.dagPath).setTransformation(
            om.MTransformationMatrix(matrix)
        )

    def resetTransformationMatrix(self) -> None:

        """
        Reset the transformation matrix

        """

        om.MFnTransform(self.dagPath).resetFromRestPosition()

    @property
    def worldMatrix(self) -> List[float]:

        """
        Get the current node s world matrix

        Returns:
            om.MMatrix: the node s world matrix
        """

        return self['worldMatrix'].value

    @worldMatrix.setter
    def worldMatrix(self, value: Union[List[float], om.MMatrix]) -> None:

        """
        Set the current node s world matrix

        Args:
            value: om.MMatrix, the matrix to set the world matrix to

        """
        if len(value) == 16:
            value = om.MMatrix(value)

        elif isinstance(value, om.MMatrix):
            value = value

        om.MFnTransform(self.dagPath).setTransformation(
            om.MTransformationMatrix(
                value * om.MMatrix(self['parentInverseMatrix'].value)
            )
        )

    @property
    def worldInverseMatrix(self) -> om.MMatrix:

        """
        Get the current node s world inverse matrix

        Returns:
            om.MMatrix: the current node s world inverse matrix

        """

        return self['worldInverseMatrix'].value

    @property
    def parentMatrix(self) -> om.MMatrix:

        """
        Get the parent world matrix of the current node

        Returns:
            om.MMatrix: the parent world matrix
        """

        return self['parentMatrix'].value

    @property
    def offsetParentMatrix(self) -> om.MMatrix:

        """
        Get the offset parent matrix of the current node

        Returns:
            om.MMatrix: the offset parent matrix
        """

        return self['offsetParentMatrix'].value

    @property
    def visibilityPlug(self) -> Plug:

        """
        Get the visibility plug of the current node

        Returns:
            Plug: the visibility plug
        """

        return self['visibility']

    @property
    def visibility(self) -> bool:

        """
        Get the visibility state of the current node

        Returns:
            bool: the visibility state
        """

        return self['visibility'].asBool()

    @visibility.setter
    def visibility(self, value: bool) -> None:

        """
        Set the visibility state of the current node

        Args:
            value: bool, the visibility state

        """

        self['visibility'] = value

    @property
    def displayLocalAxis(self) -> bool:

        """
        Get the displayLocalAxis state of the current node

        Returns:
            bool: the displayLocalAxis state
        """

        return self['displayLocalAxis'].asBool()

    @displayLocalAxis.setter
    def displayLocalAxis(self, value: bool) -> None:

        """
        Set the displayLocalAxis state of the current node

        Args:
            value: bool, the displayLocalAxis state

        """

        self['displayLocalAxis'] = value

