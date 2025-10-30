from typing import Optional, Union

from maya import cmds
from maya.api import OpenMaya as om

from ...core.abstract import dagLib
from ...core.nodeRegistry import NodeRegistry


# TODO: add useful camera properties

class Camera(dagLib.DAGNode):

    _NODE_TYPE = "camera"
    _API_TYPE = om.MFn.kCamera


NodeRegistry()[Camera.nodeType()] = Camera
