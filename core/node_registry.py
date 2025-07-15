from maya import cmds as mc
from maya.api import OpenMaya as om

from .singleton_metaclass import SingletonMeta
from .abstract import node_lib
# from .abstract import dg_lib
# from .abstract import dag_lib

__all__ = [
    'NodeRegistry',
]


class NodeRegistry(dict, metaclass=SingletonMeta):
    """
    This class is a singleton and only one instance will exist in TARLib

    ```
    # To access the registry in the TARLib module
    from TAR.TARLib import node_registry

    # add to registry
    node_registry.TarNodeRegistry()[NodeObjectType] = NodeObject

    # get from registry
    node_object = node_registry.TarNodeRegistry().get(NodeObjectType)
    ```
    """

    @staticmethod
    def ___isSubClass(cls1, cls2):
        """
        We have wierd import because of maya (and other stuff)
        So we can t use the built-in issubclass to check classes
        """
        # print(f'{repr(cls2)} - {repr(cls1.mro())}')
        return repr(cls2) in repr(cls1.mro())

    def get(self, key, default=node_lib.Node):
        if isinstance(key, (str, om.MObject)):
            return super().get(node_lib.Node(key).type, default)

        elif isinstance(key, int):
            return super().get(key, default)

        return default

    def __setitem__(self, key, value):
        if not self.___isSubClass(value, node_lib.Node):
            raise TypeError(
                f'Value must be a subclass of {node_lib.Node} got {type(value)}'
            )

        super().__setitem__(key, value)

        self.setdefault(value.__name__, {})
        self[value.__name__]['NODE_TYPE'] = key

        if value.openMayaType() is not None:
            super().__setitem__(value.openMayaType(), value)
            self[value.__name__]['API_TYPE'] = value.openMayaType()

    def show_data(self):
        for typ, obj in self.items():
            print(f'{typ:-<20}> {obj}')
