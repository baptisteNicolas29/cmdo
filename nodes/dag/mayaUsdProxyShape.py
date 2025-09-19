from typing import List, Tuple

from maya import cmds as mc
import mayaUsd.ufe as ufeUtils
import mayaUsd.lib as mayaUsdLib
from maya.api import OpenMaya as om
from pxr import Usd

from ...core.nodeRegistry import NodeRegistry
from ...core.abstract import dagLib


class MayaUsdProxyShape(dagLib.DAGNode):
    _NODE_TYPE = "mayaUsdProxyShape"
    _API_TYPE = om.MFn.kPluginShape

    @property
    def stage(self):
        """The stage property."""
        prim = mayaUsdLib.GetPrim(str(self))
        return prim.GetStage()

    @property
    def stagePath(self):
        """The stagePath property."""
        return mc.getAttr(f'{self}.filePath')

    @stagePath.setter
    def stagePath(self, value):
        mc.setAttr(f'{self}.filePath', value, typ='string')

    def getDuplicate(
            self,
            *mayaSources: Tuple[str | dagLib.DAGNode],
            parent=None
            ):

        # default to rootPrim
        if parent is None:
            parent = mayaUsdLib.GetPrim(str(self))

        parentStr = ufeUtils.usdPathToUfePathSegment(parent.GetPath())
        parentStr = parent.GetPath()
        stagePath = ufeUtils.stagePath(self.stage)
        parentFullPath = f'{stagePath},{parentStr}' if parentStr != '/' else stagePath

        longSource = mc.ls(mayaSources, l=True)

        for source in longSource:
            mc.mayaUsdDuplicate(source, parentFullPath)

    def sendDuplicate(self, *prims: Tuple[str | Usd.Prim]) -> str:

        stagePath = ufeUtils.stagePath(self.stage)

        for prim in prims:
            if isinstance(prim, Usd.Prim):
                prim = ufeUtils.usdPathToUfePathSegment(prim.GetPath())
                prim = f'{stagePath},{prim}'

            mc.mayaUsdDuplicate(prim, '|world')


NodeRegistry()[MayaUsdProxyShape.nodeType()] = MayaUsdProxyShape
