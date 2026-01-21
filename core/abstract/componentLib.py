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

        return om.MFnComponent(self)

    @property
    def componentTypeList(self) -> List[str]:


    @property
    def componentType(self) -> int:

        return self.mfnComponent.componentType