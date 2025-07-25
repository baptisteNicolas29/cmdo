from typing import List, Any, Union

from maya.api import OpenMaya as om
from maya import cmds as mc, mel

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
        animLayers = mc.ls(type='animLayer')
        if not animLayers:
            return

        # Source the mel file where the "animLayerMerge" proc is located
        mel.eval('source "performAnimLayerMerge.mel"')

        melCmd = 'animLayerMerge {%s}' % ','.join(
            [f'"{layer}"' for layer in mc.ls(type='animLayer')]
        )
        mel.eval(melCmd)

    def __init__(self, name: Union[str, om.MObject] = None) -> None:
        """
        Initialize an instance of AnimLayer

        Args:
            name: str | om.MObject, the name of the node
        """

        super().__init__(name=name)


NodeRegistry()[AnimLayer.nodeType()] = AnimLayer
