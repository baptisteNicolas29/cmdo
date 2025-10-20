from typing import Optional, Union

from maya import cmds
from maya.api import OpenMaya as om

from ...core.abstract import dagLib
from ...core.nodeRegistry import NodeRegistry


# TODO: add useful camera properties

class Camera(dagLib.DAGNode):

    _NODE_TYPE = "camera"
    _API_TYPE = om.MFn.kCamera

    def __init__(self, name: Union[str, om.MObject] = None, *args, **kwargs) -> None:

        """
        Initialize an instance of Camera

        Args:
            name: Optional[str], the name of the node
        """

        super().__init__(name=name)


NodeRegistry()[Camera.nodeType()] = Camera
