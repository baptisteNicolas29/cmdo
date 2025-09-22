from typing import Dict, Tuple, Any, Callable
from collections import OrderedDict

import sys
import inspect
import importlib

# cmds functions are added to the cmdo namespace to handle cmdo objects in & out
# mel is imported to be accessible through the cmdo namespace like: cmdo.mel
# OpenMaya, OpenMayaAnim and OpenMayaUI are imported to be accessible
#  through the cmdo namespace as om, oma and omui
from maya import cmds, mel
from maya.api import (
    OpenMaya as om,
    OpenMayaAnim as oma,
    OpenMayaUI as omui
)


__all__ = [
    'bigReload',
    'mathLib',
    'core',
    'nodes',
    'api',
    'getCmdoNodeDict'
]


# TODO: Add Undo/Redo in maya.api.OpenMaya... not looking forward to that...
#  currently the libraries that implements OpenMaya behavior doesn't support
#  undoing or redoing (so a lot of libraries),
#  in OpenMaya, Undo/Redo is managed through om.MPxCommands,
#  see a possible implementation -> https://github.com/mottosso/apiundo


__PACKAGE_NAME = __name__


# TODO: try to add reloading dependencies.
#  bigReload is a debugging function
def bigReload(module_to_reload=__PACKAGE_NAME):
    cmds.warning(
        'bigReload is a debugging function and should not be used in production'
    )
    to_reload = []
    for name, module in sys.modules.items():
        if name.startswith(module_to_reload):
            to_reload.append(module)

    for module in to_reload:
        importlib.import_module(module.__name__)
        importlib.reload(module)

    parent_module = sys.modules.get(module_to_reload)
    importlib.import_module(parent_module.__name__)
    importlib.reload(parent_module)


# Import modules to package root for easier access
#
# !!!!!!!!!! WARNING !!!!!!!!!!:
#     Order of import is important to avoid circular imports
#     or partial import errors

from . import mathLib
from . import core
from . import nodes
from . import api

from .core.exceptions import *

from .api import *
from .api.hierarchy import *
from .api.history import *
from .api.materials import *
from .api.namespace import *
from .api.uv import *
from .api.deformers import *
from .api.graph import *
from .api.plugs import *
from .api.curves import *
from .api.mesh import *
from .api.bifrost import *


def getCmdoNodeDict() -> Dict:
    """
    Get registered cmdo node classes
    Data is stored in three different ways for each node class:
        - str(mayaType): CmdoClass
        - int(mayaApiType): CmdoClass
        - CmdoClass: {"NODE_TYPE": str(mayaType), "API_TYPE": int(mayaApiType)}

    One exception is mayaApiType : om.MFn.KPluginShape->712, which will
     always default to cmdo.core.abstract.nodelib.Node because the type
     is shared across all plugin shapes

    Returns:
         dict: {id: data} multiple pairs per node representing different ids
    """
    from .core import nodeRegistry

    return nodeRegistry.NodeRegistry().copy()


def __addMayaCmdsToCmdoNamespace():
    """
    Dump all maya.cmds functions that do not exist in cmdo namespace
    Convert inputs from cmdo types to maya types
    Convert outputs from maya types to cmdo types

    """

    def _isNodeSubclass(item):
        return issubclass(type(item), core.abstract.nodeLib.Node)

    def _isGraphSubclass(item):
        return issubclass(type(item), core.graphLib.Graph)

    def _convertInputArguments(args):
        args_list = list(args)

        for i, arg in enumerate(args_list):
            if _isNodeSubclass(arg):
                args_list[i] = arg.name

            elif _isGraphSubclass(arg):
                args_list[i] = arg.getSelectionStrings()

            elif isinstance(arg, (list, tuple, set)):
                args_list[i] = _convertInputArguments(arg)

        return args_list

    def _convertOutputArguments(result: Any) -> core.abstract.nodeLib.Node | core.graphLib.Graph | Any:
        """
        Convert the maya.cmds function output to cmdo types if possible

        Args:
            result: the result of maya.cmds function

        Returns:

        """
        if isinstance(result, str) and mc.objExists(result):
            return ls(result)[0]

        elif isinstance(result, (list, tuple, set)) and all(
                mc.objExists(res) for res in result):

            return ls(*result)

        return result

    def _cmdsWrapperFunction(func: Callable) -> Callable:
        """
        A function wrapper to enable easier interaction with cmdo

        Arguments:
            func: callable, a function to wrap

        Returns:
             callable: a wrapped function
        """
        def wrap(*args, **kwargs) -> Any:
            """
            Wrapper function for cmds function to return cmdo type if possible

            """
            args_list = _convertInputArguments(args)

            result = func(*args_list, **kwargs)

            # TODO: remove debug print on release, for performance issues
            # print(
            #     f'{func.__name__} - '
            #     f'\n\t{args_list = }'
            #     f'\n\t{kwargs = }'
            #     f'\n\t{result = }'
            # )

            return _convertOutputArguments(result)

        return wrap

    # Filtering of cmds functions
    # islower() serves to filter out mel macros, we only want python compatible
    # functions in the form of function(*args, **kwargs) and not Function()
    def _filterCmds(key: Tuple) -> bool:
        """
        Filter cmds functions by key

        :param key: pair of function name and function object
        Returns:
            bool: the filtered result
        """

        return (
                key[0][0].islower()
                and callable(key[1])
                and key[1].__module__ == cmds.__name__
                and key[0] not in cmdoFunctionKeys
        )

    cmdo_module = sys.modules[__name__]
    cmdoFunctionKeys = list(cmdo_module.__dict__.keys())

    cmds_dict = OrderedDict(sorted(filter(
        _filterCmds,
        dict(inspect.getmembers(cmds)).items()
    )))

    for k, v in cmds_dict.items():
        setattr(cmdo_module, k, _cmdsWrapperFunction(v))

    print('finished adding cmds functions')


__addMayaCmdsToCmdoNamespace()

# Delete the function after using it to make it not accessible by user
# after one run of the function it has no further use for the package
del __addMayaCmdsToCmdoNamespace
