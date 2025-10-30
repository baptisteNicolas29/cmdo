from typing import Optional, List, Union

from maya.api import OpenMaya as om, OpenMayaAnim as oma

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class AnimCurve(dgLib.DGNode):

    _NODE_TYPE = "animCurve"
    _API_TYPE = om.MFn.kAnimCurve


class AnimCurveTA(AnimCurve):

    _NODE_TYPE = "animCurveTA"
    _API_TYPE = om.MFn.kAnimCurveTimeToAngular


class AnimCurveTL(AnimCurve):

    _NODE_TYPE = "animCurveTL"
    _API_TYPE = om.MFn.kAnimCurveTimeToDistance


class AnimCurveTT(AnimCurve):

    _NODE_TYPE = "animCurveTT"
    _API_TYPE = om.MFn.kAnimCurveTimeToTime


class AnimCurveTU(AnimCurve):

    _NODE_TYPE = "animCurveTU"
    _API_TYPE = om.MFn.kAnimCurveTimeToUnitless


class AnimCurveUA(AnimCurve):
    _NODE_TYPE = "animCurveUA"
    _API_TYPE = om.MFn.kAnimCurveUnitlessToAngular


class AnimCurveUL(AnimCurve):
    _NODE_TYPE = "animCurveUL"
    _API_TYPE = om.MFn.kAnimCurveUnitlessToDistance


class AnimCurveUT(AnimCurve):
    _NODE_TYPE = "animCurveUT"
    _API_TYPE = om.MFn.kAnimCurveUnitlessToTime


class AnimCurveUU(AnimCurve):
    _NODE_TYPE = "animCurveUU"
    _API_TYPE = om.MFn.kAnimCurveUnitlessToUnitless


NodeRegistry()[AnimCurve.nodeType()] = AnimCurve
NodeRegistry()[AnimCurveTA.nodeType()] = AnimCurveTA
NodeRegistry()[AnimCurveTL.nodeType()] = AnimCurveTL
NodeRegistry()[AnimCurveTT.nodeType()] = AnimCurveTT
NodeRegistry()[AnimCurveTU.nodeType()] = AnimCurveTU
NodeRegistry()[AnimCurveUA.nodeType()] = AnimCurveUA
NodeRegistry()[AnimCurveUL.nodeType()] = AnimCurveUL
NodeRegistry()[AnimCurveUT.nodeType()] = AnimCurveUT
NodeRegistry()[AnimCurveUU.nodeType()] = AnimCurveUU


# TODO: find solutions for all the different animCurve types
#  immediate solution is to subclass AnimCurve into each anim curve type
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
