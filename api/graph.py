from maya import cmds as mc

from ..core.graph_lib import Graph


__all__ = [
    'ls',
    'listRelatives',
    'listHistory',
    'createNode',
    'delete'
]


def ls(*args, **kwargs) -> Graph:

    return Graph.ls(*args, **kwargs)


def listHistory(*args, **kwargs) -> Graph:

    return Graph.listHistory(*args, **kwargs)


def listRelatives(*args, **kwargs) -> Graph:

    return Graph.listRelatives(*args, **kwargs)


def createNode(typ, name=None, parent=None, **kwargs) -> 'om.MObject':

    return Graph().createNode(typ, name=name, parent=parent, **kwargs)


def delete(*args, **kwargs) -> None:

    Graph.delete(*args, **kwargs)
