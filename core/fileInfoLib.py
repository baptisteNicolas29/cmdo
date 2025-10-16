from typing import Dict, List

from maya import cmds as mc

from .singletonMetaclass import SingletonMeta


__all__: List[str] = [
    'MayaFileInfo'
]


class MayaFileInfo(dict, metaclass=SingletonMeta):

    """
    The class is a singleton and only one will exist in cmdo
    """

    @property
    def raw_data(self) -> List:
        return mc.fileInfo(query=True)

    def get(self, key: str, default=None):

        return mc.fileInfo(key, query=True) or default

    def __getitem__(self, key: str):

        return mc.fileInfo(key, query=True)

    def __setitem__(self, key: str, value: str):
        super().__setitem__(key, value)
        super().update({key: value})

        mc.fileInfo(str(key), str(value))

    def update(self, other: Dict, **kwargs):

        if not isinstance(other, dict):
            raise TypeError(f'Need dict instance, got {type(other)}')

        for key, value in other.items():
            mc.fileInfo(str(key), str(value))

        self.clear()

        raw_data = mc.fileInfo(query=True)
        for key, value in zip(raw_data[::2], raw_data[1::2]):
            self[key] = value
            super().__setitem__(key, value)
