from typing import List

from maya import cmds


__all__: List[str] = [
    'PauseViewport'
]


class PauseViewport(object):
    """
    Context manager object that will pause Maya's viewport during execution
    """

    def __init__(self):
        super().__init__()

    def __enter__(self):
        if cmds.about(batch=True):
            return

        cmds.ogs(pause=True)
        cmds.refresh(suspend=True)

    def __exit__(self, execType, execValue, traceback):
        if cmds.about(batch=True):
            return

        cmds.ogs(pause=True)
        cmds.refresh(suspend=False)
