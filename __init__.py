from typing import List, Dict, Union

import os
import sys
import pkgutil
import inspect
import importlib
import traceback


__all__ = [
    'bigReload',
    'math',
    'core',
    'nodes',
    'api',
    'getCmdoNodeDict'
]

# TODO: Add Undo/Redo in maya.api.OpenMaya... not looking forward to that...
#  currently the library that implements OpenMaya behavior doesn't support
#  undoing or redoing


# <editor-fold desc="Package Reload">
__PACKAGE_NAME = __name__


# TODO: bigReload could be better it usually take two calls to really
#  reload the whole package

def flushImports(pckg_name: str = __PACKAGE_NAME):
    to_delete = []

    for module in sys.modules:
        if not module.startswith(pckg_name):
            continue

        to_delete.append(module)

    # print(f'Flushing package {str(pckg_name)}')
    for module in reversed(to_delete):
        # print(module)
        del sys.modules[module]


def formatPyModulePath(file_path: str, pckg_name: str = __PACKAGE_NAME) -> str:
    """
    Takes a file path and returns a formatted python path

    Args:
        file_path: the path of the py file or package to format
        pckg_name: The name of the package to format

    Returns:
        a formatted string module path (eg: package.submodule.module)
    """

    file_components = os.path.splitext(file_path)[0].split(os.sep)
    # print(f'{file_components = }')
    return '.'.join(file_components[file_components.index(pckg_name):])


def findModules(
    package_path: Union[str, List[str]],
    extensions: List[str] = None,
    exceptions: List[str] = None
) -> List[str]:
    """
    Find every file recursively in a python package

    Args:
        package_path: the path(s) to python package(s)
        extensions: extensions to search for
        exceptions: exceptions to leave out of the search

    Returns:
        a list of formatted module paths (eg: package.submodule.module)
    """
    if extensions is None:
        extensions = ['']

    if exceptions is None:
        exceptions = ['']

    modules = []

    if not isinstance(package_path, list):
        package_path = [package_path]

    # pckg_name = package_path[0].split(os.sep)[-1]
    modules.append(formatPyModulePath(package_path[0]))

    spec = pkgutil.walk_packages(path=package_path)

    if not spec:
        return []

    for (finder, name, is_package) in spec:
        path = str(os.path.join(finder.path, name))

        if not is_package:
            continue

        for d in os.listdir(path):
            if (os.path.isfile(file := os.path.join(path, d)) and
                os.path.splitext(file)[-1] in extensions and
                    d not in exceptions):

                modules.append(formatPyModulePath(file))

        modules.append(formatPyModulePath(path))

        modules.extend(
            findModules(
                [path],
                extensions=extensions,
                exceptions=exceptions
            )
        )

    return modules


def bigReload(
    package_path: Union[str, List] = None,
    flush: bool = True,
    extensions: List = None,
    exceptions: List = None,
    feedback: bool = False
) -> None:
    """
    Reloads all packages and modules found inside a package

    Args:
        package_path: the path of the package to reload
        flush: whether to flush the given package or not
        extensions: all extensions to reload (should be python extensions)
        exceptions: all exceptions to leave out of reload
        feedback: whether to print the reload or not
    Returns:

    """

    # print(
    #     f'{package_path = }\n'
    #     f'{flush = }\n'
    #     f'{extensions = }\n'
    #     f'{exceptions = }\n'
    #     f'{feedback = }\n'
    # )

    if package_path is None:
        current_frame = inspect.currentframe()
        package_path = os.path.dirname(inspect.getfile(current_frame))

    if flush:
        package_name = os.path.splitext(package_path)[0].split(os.sep)[-1]
        flushImports(package_name)

    extensions = [] if extensions is None else extensions
    exceptions = [] if exceptions is None else exceptions

    extensions += ['.py']
    exceptions += ['__init__.py']

    modules = findModules(
        package_path,
        extensions=extensions,
        exceptions=exceptions
    )

    module_load_errors = 0
    error_messages = []
    for path in modules:
        if feedback:
            print(f'\nPath to import {path}')
        try:
            module = importlib.import_module(path)

            importlib.reload(module)
            if feedback:
                print(f'\tRELOADED : {module}')

        except ModuleNotFoundError as mnfe:
            module_load_errors += 1
            message = f'Module not found {path}\nModuleNotFoundError: {mnfe}'
            error_messages.append(message)
            # traceback.print_exc()
            if feedback:
                print(message)

        except Exception as e:
            module_load_errors += 1
            message = f'Error Reloading / Importing {path}\nException: {e}'
            error_messages.append(message)
            # traceback.print_exc()
            if feedback:
                print(message)

    print(
        f'\n{__PACKAGE_NAME} RELOADED :'
        f'\n\t- {len(modules)} modules / packages'
        f'\n\t- {module_load_errors} errors while reloading\n'
    )
    for message in error_messages:
        print(f'{"-"*10}\n{message}')
# </editor-fold>


"""
Import modules to package root for easier access

WARNING:
    Order of import is important to avoid circular imports
    or partial import errors
"""


from . import math_lib as math
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

    Returns:
         dict: {id: data} multiple pairs per node representing different ids
    """
    from .core import nodeRegistry

    return nodeRegistry.NodeRegistry().copy()
