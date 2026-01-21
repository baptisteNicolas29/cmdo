from typing import List, Union

from maya.api import OpenMaya as om

from ...core.abstract import geometryFilterLib
from ...core.nodeRegistry import NodeRegistry


# TODO: I don t want to do it yet...
#  it's such an annoying deformer in maya commands
class BlendShape(geometryFilterLib.GeometryFilter):

    _NODE_TYPE = 'blendShape'
    _API_TYPE = om.MFn.kBlendShape

    # TODO: move transfer to api
    def transferTo(self, arg: Union[str, om.MObject]):
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

    def getTarget(self, arg: Union[int, str]):
        return NotImplementedError(f'Get target {arg}')

    def addTarget(self, arg: Union[str, om.MObject]):
        return NotImplementedError(f'Adding target {arg}')

    def removeTarget(self, target_index: Union[int, str]):
        return NotImplementedError(f'Removing target {target_index}')

    def resetAllTargetWeights(self):
        return NotImplementedError('resetting all targets')

    def resetTargetWeight(self, arg: Union[int, str]):
        return NotImplementedError(f'Resetting target from idx {arg}')

    # TODO: maybe rebuild functions move to api as well
    def rebuildAllTargets(self):
        return NotImplementedError(f'Rebuilding all target')

    def rebuildTarget(self, arg: Union[int, str]):
        return NotImplementedError(f'Rebuilding target {arg}')


NodeRegistry()[BlendShape.nodeType()] = BlendShape

