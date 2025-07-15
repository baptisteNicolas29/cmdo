from typing import List

from maya.api import OpenMaya as om

from ...core.abstract import dg_lib
from ...core.node_registry import NodeRegistry


# TODO: I don t want to do it yet... is such an annoying deformer in maya script
class BlendShape(dg_lib.DGNode):

    _NODE_TYPE = 'blendShape'
    _API_TYPE = om.MFn.kBlendShape

    def __init__(self, name: str | om.MObject = None) -> None:
        """
        Initialize an instance of BlendShape

        Args:
            name: str | om.MObject, the name of the node
        """

        super().__init__(name=name)

    # TODO: move transfer to api
    def transfer_to(self, arg: str | om.MObject):
        return NotImplementedError(f'Transferring target to obj {arg}')

    @property
    def targetCount(self) -> int:
        return NotImplementedError(f'Getting target count')

    @property
    def targets(self):
        return NotImplementedError(f'Getting target idx')

    @property
    def targetNames(self) -> List[str]:
        return NotImplementedError(f'Getting target names')

    def getTarget(self, arg: int | str):
        return NotImplementedError(f'Get target {arg}')

    def addTarget(self, arg: str | om.MObject):
        return NotImplementedError(f'Adding target {arg}')

    def removeTarget(self, target_index: int | str):
        return NotImplementedError(f'Removing target {target_index}')

    def resetAllTargetWeights(self):
        return NotImplementedError('resetting all targets')

    def resetTargetWeight(self, arg: int | str):
        return NotImplementedError(f'Resetting target from idx {arg}')

    # TODO: maybe rebuild functions move to api as well
    def rebuildAllTargets(self):
        return NotImplementedError(f'Rebuilding all target')

    def rebuildTarget(self, arg: int | str):
        return NotImplementedError(f'Rebuilding target {arg}')


NodeRegistry()[BlendShape.nodeType()] = BlendShape

