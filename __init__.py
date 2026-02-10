from typing import Dict, Tuple, Any, Callable, List, Generator, Union, Type
from collections import OrderedDict

import sys
from types import ModuleType, FunctionType
import inspect
import importlib
import contextlib

# - cmds functions are added to the cmdo namespace
#    to handle cmdo objects in & out conversion
# - mel is imported to be accessible through the cmdo namespace
#    like: cmdo.mel
# - OpenMaya, OpenMayaAnim and OpenMayaUI are imported to be accessible
#    through the cmdo namespace as om, oma and omui
#    like: cmdo.om, cmdo.oma, cmdo.omui
from maya import cmds, mel
from maya.api import (
    OpenMaya as om,
    OpenMayaAnim as oma,
    OpenMayaUI as omui
)


__all__: List[str] = [
    'core',
    'nodes',
    'api',
    'getCmdoNodeDict',
    'bigReload',
    'getDebugMode',
    'setDebugMode',
    'debugContext'
]


# TODO: Add Undo/Redo using maya.api.OpenMaya... not looking forward to that...
#  currently the libraries that implements OpenMaya behavior don't support
#  undoing or redoing (so a lot of libraries),
#  in OpenMaya, Undo/Redo is managed through om.MPxCommands,
#  see a possible implementation -> https://github.com/mottosso/apiundo


# current package name
__PACKAGE_NAME: str = __name__

# __CMDS_DEBUG_PRINT: True/False,
#   whether to print maya.cmds function's name/input/output/result
# If __CMDS_DEBUG_MAX_PRINT is set to -1,
#  the debug print will not trim the message
#  this can become a problem when printing very large data sets (eg: meshes)
__CMDS_DEBUG_PRINT: bool = False
__CMDS_DEBUG_MAX_PRINT: int = 1000


# TODO: try to add reloading dependencies to bigReload

# bigReload is a debugging function and
#  should not be used in production
def bigReload(moduleToReload: Union[str, FunctionType, ModuleType] = __PACKAGE_NAME, feedback: bool = False) -> None:
    """
    Reload the given package from name and all its children modules

    :param moduleToReload: str, the name of the package/module to reload
    :param feedback: bool, whether to print which module is reloaded

    """

    if isinstance(moduleToReload, FunctionType):
        moduleToReload = moduleToReload.__module__.split('.')[0]

    elif isinstance(moduleToReload, ModuleType):
        moduleToReload = moduleToReload.__package__.split('.')[0]

    cmds.warning(
        'cmdo.bigReload is a debugging function and '
        'should not be used in production'
    )

    if isinstance(moduleToReload, FunctionType):
        moduleToReload = moduleToReload.__module__.split('.')[0]

    elif isinstance(moduleToReload, ModuleType):
        moduleToReload = moduleToReload.__package__.split('.')[0]

    toReload = []
    for name, module in sys.modules.items():
        if name.startswith(moduleToReload):
            toReload.append(module)

    for module in toReload:
        print(
            f'Import/Reload : {module.__name__:-<40} - {str(module)}'
        ) if feedback else None
        importlib.import_module(module.__name__)
        importlib.reload(module)

    parentModule = sys.modules.get(moduleToReload)
    print(
        f'Import/Reload : {parentModule.__name__:-<40} - {str(parentModule)}'
    ) if feedback else None
    importlib.import_module(parentModule.__name__)
    importlib.reload(parentModule)


# Import modules to package root for easier access
#
# !!!!!!!!!! WARNING !!!!!!!!!!
#     Order of import is important to avoid circular imports
#     or partial import errors, until we get lazy imports

from . import core
from . import nodes
from . import api

from .core.cmdoTyping import *
from .core.openMayaTypes import *
from .core.exceptions import *

# Basic cmdo node Typing
from .core.plugsLib import PlugType, PlugArrayType
from .core.abstract.nodeLib import NodeType
from .core.abstract.dgLib import DGType
from .core.abstract.dagLib import DAGType
from .core.graphLib import GraphType

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

    :return: dict: {id: data} multiple pairs per node representing different ids

    """
    from .core import nodeRegistry

    return nodeRegistry.NodeRegistry().copy()


def getDebugMode() -> bool:
    """
    Get the debug mode state

    :return: bool: the current state of the debug mode

    """

    cmds.warning(
        'cmdo.getDebugMode is a debugging function and '
        'should not be used in production'
    )

    global __CMDS_DEBUG_PRINT

    return __CMDS_DEBUG_PRINT


def setDebugMode(state: bool = False, maxCharCount: int = __CMDS_DEBUG_MAX_PRINT) -> None:
    """
    Set the debug mode on/off

    !!!! WARNING !!!! - state=True, prints on every use of maya.cmds functions
     Should not be use outside of dev contexts

    :param state: bool, the state of the debug mode to set
    :param maxCharCount: int, the maximum number of string characters per print
        if set to -1, will print all given characters

    """

    cmds.warning(
        'cmdo.setDebugMode is a debugging function and '
        f'should not be used in production: {state = }'
    )

    global __CMDS_DEBUG_PRINT
    global __CMDS_DEBUG_MAX_PRINT

    __CMDS_DEBUG_PRINT = state
    __CMDS_DEBUG_MAX_PRINT = maxCharCount

    cmds.warning(f'{__CMDS_DEBUG_PRINT = }')
    cmds.warning(f'{__CMDS_DEBUG_MAX_PRINT = }')


@contextlib.contextmanager
def debugContext(state: bool = False, maxCharCount: int = __CMDS_DEBUG_MAX_PRINT) -> Generator:
    """
    Set the debug mode on/off, at exit of the context, reset to previous value

    !!!! WARNING !!!! - prints on every use of maya.cmds functions
     Should not be use outside of dev contexts

    :param state: bool, the state of the debug mode to set
    :param maxCharCount: int, the maximum number of string characters per print

    """

    cmds.warning(
        'cmdo.debugContext is a debugging function and '
        f'should not be used in production: {state = }'
    )

    global __CMDS_DEBUG_PRINT
    global __CMDS_DEBUG_MAX_PRINT

    tempDebugValue = __CMDS_DEBUG_PRINT
    tempDebugMaxCount = __CMDS_DEBUG_MAX_PRINT

    __CMDS_DEBUG_PRINT = state
    __CMDS_DEBUG_MAX_PRINT = maxCharCount
    cmds.warning(f'{__CMDS_DEBUG_PRINT = }')
    cmds.warning(f'{__CMDS_DEBUG_MAX_PRINT = }')

    yield

    __CMDS_DEBUG_PRINT = tempDebugValue
    __CMDS_DEBUG_MAX_PRINT = tempDebugMaxCount


def __debugPrint(message: str) -> None:
    """
    Print the given message if the debug mode is True
    This is mostly used to print wrapped functions from
     the maya.cmds & maya.mel modules

    :param message: str, the message to print

    """

    global __CMDS_DEBUG_PRINT
    if not __CMDS_DEBUG_PRINT:
        return

    if __CMDS_DEBUG_MAX_PRINT != -1 and len(message) > __CMDS_DEBUG_MAX_PRINT:
        message = f'{message[:__CMDS_DEBUG_MAX_PRINT]}....'

    print(message)


def __addMayaCmdsToCmdoNamespace() -> None:
    """
    Dump all maya.cmds functions that do not exist in cmdo namespace

    Wrap maya.cmds functions to:
        Convert inputs from cmdo types to maya types
        Convert outputs from maya types to cmdo types

    """

    def _isNodeSubclass(item: Any) -> bool:
        """Check if item is a subclass of nodeLib.Node"""
        return issubclass(type(item), core.abstract.nodeLib.Node)

    def _isPlugSubclass(item: Any) -> bool:
        """Check if item is a subclass of plugsLib.Plug"""
        return issubclass(type(item), core.plugsLib.Plug)

    def _isGraphSubclass(item: Any) -> bool:
        """Check if item is a subclass of graphLib.Graph"""
        return issubclass(type(item), core.graphLib.Graph)

    def _convertInputArguments(args: Any) -> List:
        """
        Convert the given arguments to str for maya.cmds if possible

        :param args: Any, arguments to convert to str for maya.cmds

        :return: List[str]: the converted arguments for maya.cmds

        """

        argsList = list(args)

        for i, arg in enumerate(argsList):
            if _isNodeSubclass(arg):
                argsList[i] = arg.name

            elif _isPlugSubclass(arg):
                argsList[i] = arg.name()

            elif _isGraphSubclass(arg):
                argsList[i] = arg.getSelectionStrings()

            elif isinstance(arg, (list, tuple, set)):
                argsList[i] = _convertInputArguments(arg)

        return argsList

    cmdoResultType = Type[Union[core.Node, om.MObject, core.Graph, Any]]

    def _convertOutputArguments(result: Any) -> cmdoResultType:
        """
        Convert the maya.cmds function output to cmdo types if possible

        :param result: Any, the result of maya.cmds function

        :return: cmdoResultType: cmdo object or base result if conversion failed

        """

        if isinstance(result, str) and cmds.objExists(result):
            return ls(result)[0]

        elif isinstance(result, (list, tuple, set)) and all(cmds.objExists(str(res)) for res in result):
            return ls(*result)

        return result

    def _cmdsWrapperFunction(func: Callable) -> Callable:
        """
        A function wrapper to enable easier interaction with cmdo

        :param func: callable, a function to wrap

        :return: callable, a wrapped function

        """
        def wrap(*args, **kwargs) -> Any:
            """
            Wrapper function for cmds function to return cmdo type if possible

            """
            argsList = _convertInputArguments(args)

            result = func(*argsList, **kwargs)

            __debugPrint(
                f'{func.__name__} - '
                f'\n\t{argsList = }'
                f'\n\t{kwargs = }'
                f'\n\t{result = }'
            )

            return _convertOutputArguments(result)

        return wrap

    # Filtering of cmds functions
    # islower() serves to filter out mel macros, we only want python compatible
    # functions in the form of function(*args, **kwargs) and not Function()
    def _filterCmds(key: Tuple) -> bool:
        """
        Filter cmds functions by key

        :param key: a pair containing function name and function object

        :return: bool: the filtered result

        """

        return (
                key[0][0].islower()
                and callable(key[1])
                and key[1].__module__ == cmds.__name__
                and key[0] not in cmdoFunctionKeys
        )

    cmdoModule = sys.modules[__name__]
    cmdoFunctionKeys = list(cmdoModule.__dict__.keys())

    cmdsDict = OrderedDict(sorted(filter(
        _filterCmds,
        dict(inspect.getmembers(cmds)).items()
    )))

    for key, value in cmdsDict.items():
        setattr(cmdoModule, key, _cmdsWrapperFunction(value))

    __debugPrint('finished adding cmds functions')


# Add wrapped maya.cmds functions to cmdo package
__addMayaCmdsToCmdoNamespace()

# Delete the function after using it to make it un-accessible by user
# after one run of the function it has no further use for the package
del __addMayaCmdsToCmdoNamespace
