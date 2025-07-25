from ..core.graphLib import Graph


# * import list
__all__ = [
    'lockTransforms',
    'hideTransforms',
    'lockAndHideTransforms'
]


def lockTransforms(nodes, attrs=None, value: bool = True) -> None:
    """
    Lock the transform attributes of given node(s)

    :param nodes:
    :param attrs:
    :param value:
    :return:
    """
    graph_node = Graph.ls(nodes)
    for node in graph_node:
        attributes = [node[attr] for attr in attrs] or node.transformAttributes

        for attr in attributes:
            attr.isLocked = value


def hideTransforms(nodes, attrs=None, value: bool = True) -> None:
    """
    Hide the transform attributes of given node(s)

    :param nodes:
    :param attrs:
    :param value:
    :return:
    """
    graph_node = Graph.ls(nodes)
    for node in graph_node:
        attributes = [node[attr] for attr in attrs] or node.transformAttributes

        for attr in attributes:
            attr.isKeyable = not value


def lockAndHideTransforms(nodes, attrs=None, value: bool = True) -> None:
    """
    Lock and Hide the transform attributes of given node(s)

    :param nodes:
    :param attrs:
    :param value:
    :return:
    """

    graph_node = Graph.ls(nodes)
    for node in graph_node:
        attributes = (
            [node[attr] for attr in attrs]
            if attrs
            else node.transformAttributes
        )

        for attr in attributes:
            print(attr)
            attr.isLocked = value
            attr.isKeyable = not value
