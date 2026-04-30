from typing import Dict, List
import itertools

from maya import cmds

from .singletonMetaclass import SingletonMeta


__all__: List[str] = [
    'MayaFileInfo'
]


class MayaFileInfo(dict, metaclass=SingletonMeta):

    """
    The class is a singleton and only one should exist in cmdo

    This class manages mayaFileInfo in an easier way
    """

    def __init__(self):
        super().__init__()

        # makes key value pairs with every two element of the list
        # eg: ['application', 'maya', 'product', 'Maya 2024', ...]
        # -> zip(('application', 'maya'), ('product', 'Maya 2024'), ...)
        for (key, value) in zip(*[iter(cmds.fileInfo(query=True))] * 2):
            self[key] = value

    @property
    def raw_data(self) -> List:

        return cmds.fileInfo(query=True)

    def get(self, key: str, default=None):

        return cmds.fileInfo(key, query=True) or default

    def __getitem__(self, key: str):

        return cmds.fileInfo(key, query=True)

    def __setitem__(self, key: str, value: str):
        super().__setitem__(key, value)
        super().update({key: value})

        cmds.fileInfo(str(key), str(value))

    def remove(self) -> None: ...

    def pop(self, key: str, default=None):
        value = self.pop(key, default=default)
        cmds.fileInfo(remove=key)

        return value

    def popitem(self):
        key, value = self.popitem()
        cmds.fileInfo(remove=key)

        return {key: value}

    def update(self, other: Dict, **kwargs):

        if not isinstance(other, dict):
            raise TypeError(f'Need dict instance, got {type(other)}')

        for key, value in other.items():
            cmds.fileInfo(str(key), str(value))

        self.clear()

        raw_data = cmds.fileInfo(query=True)
        for key, value in zip(raw_data[0::2], raw_data[1::2]):
            self[key] = value
            super().__setitem__(key, value)
