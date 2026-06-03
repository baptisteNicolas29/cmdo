from typing import Optional, Union, List, Set, Type

from maya.api import OpenMaya as om, OpenMayaAnim as oma

from ..cmdoTyping import CmdoObject
from . import dgLib
from ...core import graphLib


"""
import cmdo
cmdo.bigReload()
from cmdo.core.abstract import componentLib

selection = cmdo.cmds.ls('l_arm:chain00_ctrl.cv[0:2]', 'l_arm:chain00_ctrl.cv[7]')
mSel = cmdo.MSelectionList()
for sel in selection:
    mSel.add(sel)
    
print(f'Selection strings: {mSel.getSelectionStrings()}')

for i in range(mSel.length()):
    print(mSel.getComponent(i))

mdag, mobj = mSel.getComponent(0)

mdag.fullPathName()
mobj.apiTypeStr

component = cmdo.om.MFnComponent(mobj)
component.componentType == cmdo.om.MFn.kCurveCVComponent
component.elementCount
componentLib.Component.__subclasses__()

comp = componentLib.Component('c_body_mshShape.e[*]')
comp.mfnComponent.type()
comp.elementCount


selection = cmdo.cmds.ls('l_arm:chain00_ctrl.cv[0:2]', 'l_arm:chain00_ctrl.cv[7]')
mSel = cmdo.MSelectionList()
for sel in selection:
    mSel.add(sel)

print(f'{mSel.length() = }')
mItSel = cmdo.om.MItSelectionList(mSel)
mItSel.hasComponents()
for i in range(mSel.length()):
    print(f'{mItSel.getStrings() = }')
    mDag, mObj = mItSel.getComponent()
    print(f'{mItSel.getComponent() = }')
    
    fn_vertices = cmdo.om.MFnSingleIndexedComponent(mObj)
    print(f'{fn_vertices.getElements() = }')
"""

# TODO:
#  MFnSingleIndexedComponents -> vertices, faces, edges, cvs
#  MFnDoubleIndexedComponent -> surface cvs
#  MFnTripleIndexedComponent -> lattice points


class Components(om.MObject):

    _API_TYPE = om.MFn.kComponent

    @classmethod
    def openMayaType(cls) -> int:
        """
        Internal OpenMaya type

        :return: int, the OpenMaya type
        """

        return cls._API_TYPE

    @classmethod
    def getComponent(cls, name: CmdoObject):

        component = cls(name)

        for subclass in cls.__subclasses__():
            if not component.componentType == subclass.openMayaType():
                continue

            return subclass(name)

        return component

    def __init__(self, name: CmdoObject = None) -> None:

        """
        Initialize an instance of Node

        :param name: CmdoObject, the name of the node
        """

        if isinstance(name, str):

            sel_list = om.MSelectionList()
            sel_list.add(name)
            mDag, mObj = sel_list.getComponent(0)
            super().__init__(mObj)

        elif isinstance(name, om.MObject):
            super().__init__(name)

        self.__component = om.MFnComponent(self)

    @property
    def mfnComponent(self) -> om.MFnComponent:
        """
        Get mfnComponent of the om.MObject

        :return: om.MFnComponent, the component object
        """

        return self.__component

    # @property
    # def name(self) -> str:

    @property
    def componentTypeList(self) -> List[str]:
        """
        A list of possible Component types

        :return: List[str], the list of possible component types
        """

        raise NotImplementedError('WIP')

    @property
    def componentType(self) -> int:
        """
        Which type of elements are stored in this Component object

        :return:
        """

        return self.mfnComponent.componentType

    @property
    def elementCount(self) -> int:
        """
        The number of elements in the Component object

        :return: int, the number of elements in the Component object
        """

        return self.mfnComponent.elementCount

    @property
    def isComplete(self) -> bool:
        """
        If this Component object represents the full set of elements,

        from index 0 to -1

        :return: bool, if this Component object represents all elements
        """

        return self.mfnComponent.isComplete

    @property
    def isEmpty(self) -> bool:
        """
        If this Component object has no elements

        :return: bool, if this Component object has no elements
        """

        return self.mfnComponent.isEmpty


class MeshVertexComponent(Components):
    _API_TYPE = om.MFn.kMeshEdgeComponent
    pass


class MeshEdgeComponent(Components):
    _API_TYPE = om.MFn.kMeshEdgeComponent
    pass


class MeshFaceComponent(Components):
    _API_TYPE = om.MFn.kMeshEdgeComponent
    pass


class CurveCvComponent(Components):
    _API_TYPE = om.MFn.kCurveCVComponent
    pass


class SurfaceCvComponent(Components):
    _API_TYPE = om.MFn.kSurfaceCVComponent
    pass
