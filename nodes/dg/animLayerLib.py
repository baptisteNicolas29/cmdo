from typing import List, Any, Union

from maya import cmds, mel
from maya.api import OpenMaya as om

from ...core.abstract import dgLib, dagLib
from ...core.nodeRegistry import NodeRegistry


class AnimLayer(dgLib.DGNode):

    _NODE_TYPE = "animLayer"
    _API_TYPE = om.MFn.kAnimLayer

    @staticmethod
    def mergeLayers() -> None:
        """
        Just keeping the code somewhere.
        This mel commande will merge all anim layers
        The command looks like this (admitting we have 3 animation layers)
        -> animLayerMerge {"AnimLayer1","AnimLayer2","BaseAnimation"}
        """
        animLayers = cmds.ls(type='animLayer')
        if not animLayers:
            return

        # Source the mel file where the "animLayerMerge" proc is located
        mel.eval('source "performAnimLayerMerge.mel"')

        melCmd = 'animLayerMerge {%s}' % ','.join(
            [f'"{layer}"' for layer in cmds.ls(type='animLayer')]
        )
        mel.eval(melCmd)


NodeRegistry()[AnimLayer.nodeType()] = AnimLayer
