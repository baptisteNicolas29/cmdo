from maya.api import OpenMaya as om

from .singletonMetaclass import SingletonMeta
from .abstract import nodeLib


__all__ = [
    'NodeRegistry',
]


# TODO: add entry override security
#  (ie: register a new Transform class that overrides the existing one)
class NodeRegistry(dict, metaclass=SingletonMeta):
    """
    This class is a singleton and only one instance will exist in cmdo

    ```
    # To access the registry from cmdo #
    from cmdo.core import nodeRegistry

    # add to registry #
    nodeRegistry.NodeRegistry()[NodeObjectType] = NodeObject

    # get from registry #
    node_object = nodeRegistry.NodeRegistry().get(
        NodeObjectType,
        default=DefaultReturnTypeClass
    )

    # print/get a copy of the registry
    print(cmdo.getCmdoNodeDict())
    ```
    """

    @staticmethod
    def __isSubClass(cls1, cls2):
        """
        We have wierd import because of maya (and other stuff)
        So we can t use the built-in issubclass to check classes
        """
        # print(f'{repr(cls2)} - {repr(cls1.mro())}')
        return repr(cls2) in repr(cls1.mro())

    def get(self, key, default=nodeLib.Node):
        if isinstance(key, (str, om.MObject)):
            return super().get(nodeLib.Node(key).type, default)

        elif isinstance(key, int):
            return super().get(key, default)

        return default

    def __setitem__(self, key, value):
        if not self.__isSubClass(value, nodeLib.Node):
            raise TypeError(
                f'Value must be a subclass of {nodeLib.Node} got {type(value)}'
            )

        super().__setitem__(key, value)

        self.setdefault(value.__name__, {})
        self[value.__name__]['NODE_TYPE'] = key

        if value.openMayaType() is None:
            return

        match value.openMayaType():
            case om.MFn.kPluginShape:
                super().__setitem__(value.openMayaType(), nodeLib.Node)
            case _:
                super().__setitem__(value.openMayaType(), value)

        self[value.__name__]['API_TYPE'] = value.openMayaType()

    def show_data(self):
        for typ, obj in self.items():
            print(f'{typ:-<20}> {obj}')
