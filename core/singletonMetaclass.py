__all__ = [
    'SingletonMeta'
]


class SingletonMeta(type):
    """
    This metaclass makes the child class a singleton by always returning
    the same class instance if one exists
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance

        return cls._instances[cls]
