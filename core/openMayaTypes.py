from typing import List

from maya.api import OpenMaya as om


__all__: List[str] = [
    'MSpace',
    'MObjectArray',
    'MMatrix',
    'MMatrixArray',
    'MTransformationMatrix',
    'MVector',
    'MVectorArray',
    'MPoint',
    'MPointArray',
    'MQuaternion',
    'MEulerRotation',
    'MAngle',
]

MSpace = om.MSpace

MObjectArray = om.MObjectArray

MMatrix = om.MMatrix

MMatrixArray = om.MMatrixArray

MTransformationMatrix = om.MTransformationMatrix

MVector = om.MVector

MVectorArray = om.MVectorArray

MPoint = om.MPoint

MPointArray = om.MPointArray

MQuaternion = om.MQuaternion

MEulerRotation = om.MEulerRotation

MAngle = om.MAngle

