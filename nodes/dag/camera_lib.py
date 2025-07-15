from typing import Optional

from maya import cmds as mc
from maya.api import OpenMaya as om

from ...core.abstract import dag_lib
from ...core.node_registry import NodeRegistry


# TODO: add useful camera properties

class Camera(dag_lib.DAGNode):

    _NODE_TYPE = "camera"
    _API_TYPE = om.MFn.kCamera

    def __init__(self, name: Optional[str] = None, *args, **kwargs) -> None:

        """
        Initialize an instance of Camera

        Args:
            name: Optional[str], the name of the node
        """

        super().__init__(name=name)


NodeRegistry()[Camera.nodeType()] = Camera
