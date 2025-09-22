from typing import List, Tuple

from maya import cmds as mc
from maya.api import OpenMaya as om

import mayaUsd.ufe as ufeUtils
import mayaUsd.lib as mayaUsdLib

from pxr import Usd

from ...core.nodeRegistry import NodeRegistry
from ...core.abstract import dagLib


class MayaUsdProxyShape(dagLib.DAGNode):
    _NODE_TYPE = "mayaUsdProxyShape"
    _API_TYPE = om.MFn.kPluginShape

    @property
    def stage(self):
        """The stage property."""
        prim = mayaUsdLib.GetPrim(self.fullName)
        return prim.GetStage()

    @property
    def stagePath(self):
        """The stagePath property."""
        return mc.getAttr(f'{self.fullName}.filePath')

    @stagePath.setter
    def stagePath(self, value):
        mc.setAttr(f'{self.fullName}.filePath', value, type='string')

    def getDuplicate(
        self,
        *mayaSources: Tuple[str | dagLib.DAGNode],
        parent=None
    ) -> None:

        # default to rootPrim
        if parent is None:
            parent = mayaUsdLib.GetPrim(self.fullName)

        parentStr = ufeUtils.usdPathToUfePathSegment(parent.GetPath())
        parentStr = parent.GetPath()
        stagePath = ufeUtils.stagePath(self.stage)
        parentFullPath = f'{stagePath},{parentStr}' if parentStr != '/' else stagePath

        longSource = mc.ls(*mayaSources, long=True)

        for source in longSource:
            mc.mayaUsdDuplicate(source, parentFullPath)

    def sendDuplicate(self, *prims: Tuple[str | Usd.Prim]) -> None:

        stagePath = ufeUtils.stagePath(self.stage)

        for prim in prims:
            if isinstance(prim, Usd.Prim):
                prim = ufeUtils.usdPathToUfePathSegment(prim.GetPath())
                prim = f'{stagePath},{prim}'

            mc.mayaUsdDuplicate(prim, '|world')


NodeRegistry()[MayaUsdProxyShape.nodeType()] = MayaUsdProxyShape
