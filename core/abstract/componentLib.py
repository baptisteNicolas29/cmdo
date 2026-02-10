from typing import Optional, Union, List, Set, Type

from maya.api import OpenMaya as om, OpenMayaAnim as oma

from . import dgLib
from ...core import graphLib


"""
mesh = cmdo.MSelectionList().add('c_body_mshShape.e[*]')
print(mesh.getSelectionStrings())

mdag, mobj = mesh.getComponent(0)
mdag.partialPathName()
mobj.apiTypeStr

component = cmdo.om.MFnComponent(mobj)

component.componentType
"""


class Component(om.MObject):

    @property
    def mfnComponent(self) -> om.MFnComponent:
        """
        Get mfnComponent of the om.MObject

        :return: om.MFnComponent, the component object
        """

        return om.MFnComponent(self)

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
