from typing import List, Tuple, Union

from maya import cmds
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

        return cmds.getAttr(f'{self.fullName}.filePath')

    @stagePath.setter
    def stagePath(self, value):
        """The stagePath property setter."""

        cmds.setAttr(f'{self.fullName}.filePath', value, type='string')

    def getDuplicate(
        self,
        *mayaSources: Tuple[Union[str, dagLib.DAGNode]],
        parent=None
    ) -> None:
        """

        :param mayaSources:
        :param parent:

        :return:
        """

        # default to rootPrim
        if parent is None:
            parent = mayaUsdLib.GetPrim(self.fullName)

        parentStr = ufeUtils.usdPathToUfePathSegment(parent.GetPath())
        parentStr = parent.GetPath()
        stagePath = ufeUtils.stagePath(self.stage)
        parentFullPath = f'{stagePath},{parentStr}' if parentStr != '/' else stagePath

        longSource = cmds.ls(*mayaSources, long=True)

        for source in longSource:
            cmds.mayaUsdDuplicate(source, parentFullPath)

    def sendDuplicate(self, *prims: Tuple[Union[str, dagLib.DAGNode]]) -> None:
        """

        :param prims:

        :return:
        """

        stagePath = ufeUtils.stagePath(self.stage)

        for prim in prims:
            if isinstance(prim, Usd.Prim):
                prim = ufeUtils.usdPathToUfePathSegment(prim.GetPath())
                prim = f'{stagePath},{prim}'

            cmds.mayaUsdDuplicate(prim, '|world')


NodeRegistry()[MayaUsdProxyShape.nodeType()] = MayaUsdProxyShape
