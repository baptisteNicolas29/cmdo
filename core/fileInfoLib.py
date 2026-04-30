from typing import Dict, List, Tuple

from maya import cmds


__all__: List[str] = [
    'MayaFileInfo'
]


class MayaFileInfo(dict):
    """
    This class manages mayaFileInfo in an easier way
    """

    def __init__(self):
        super().__init__()

        for (key, value) in self.formattedData:
            self[key] = value

    @property
    def rawData(self) -> List:
        """
        Return the data formatted like maya would

        :return: list[str]
        """

        return cmds.fileInfo(query=True)

    @property
    def formattedData(self) -> List[Tuple]:
        """
        Makes key value pairs with every two element of the list

        eg: ['application', 'maya', 'product', 'Maya 2024', ...]
        -> zip(('application', 'maya'), ('product', 'Maya 2024'), ...)

        :return: List[Tuple], key-value pairs for maya fileInfo
        """

        return list(zip(*[iter(self.rawData)] * 2))

    def get(self, key: str, default=None):

        return cmds.fileInfo(key, query=True) or default

    def __getitem__(self, key: str):

        return cmds.fileInfo(key, query=True)

    def __setitem__(self, key: str, value: str):
        super().__setitem__(key, value)
        super().update({key: value})

        cmds.fileInfo(str(key), str(value))

    def pop(self, key: str, default=None):
        value = self.pop(key, default=default)
        cmds.fileInfo(remove=key)

        return value

    def popitem(self):
        key, value = self.popitem()
        cmds.fileInfo(remove=key)

        return {key: value}

    def update(self, other: Dict, **kwargs):

        if not issubclass(other.__class__, dict):
            raise TypeError(f'Need dict instance, got {type(other)}')

        for key, value in other.items():
            cmds.fileInfo(str(key), str(value))

        self.clear()

        for (key, value) in self.formattedData:
            self[key] = value
            super().__setitem__(key, value)
