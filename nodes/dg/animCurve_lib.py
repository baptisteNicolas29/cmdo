from typing import Optional, List, Union

from maya.api import OpenMaya as om, OpenMayaAnim as oma

from ...core.abstract import dg_lib
from ...core.node_registry import NodeRegistry


class AnimCurve(dg_lib.DGNode):

    _NODE_TYPE = "animCurve"
    _API_TYPE = om.MFn.kAnimCurve

    def __init__(self, name: Union[str, om.MObject] = None) -> None:

        """
        Initialize an instance of Absolute

        Args:
            name: str | om.MObject, the name of the node
        """

        super().__init__(name=name)


NodeRegistry()[AnimCurve.nodeType()] = AnimCurve


# TODO: find solutions for all the different animCurve types
"""
# 8 different animCurve types that do not correspond to the apiType
# when using animCurveType property

def sortKey(x):
    return oma.MFnAnimCurve(
        om.MSelectionList().add(x).getDependNode(0)
    ).animCurveType

for ac in sorted(mc.ls(sl=True), key=sortKey):
    node_type = mc.nodeType(ac, derived=True)
    print(node_type)
    crvMObj = om.MSelectionList().add(ac).getDependNode(0)
    mfnAnim = oma.MFnAnimCurve(crvMObj)
    print(f'\t{mfnAnim.animCurveType = }\n')
    
    
print(mc.nodeType(mc.ls(sl=True)[0], inherited=True)[-2])
"""
