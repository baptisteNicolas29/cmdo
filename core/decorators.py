from typing import Callable

import io
import time
import pstats
import cProfile
import traceback
from pstats import SortKey
from functools import wraps

from maya import cmds


# TODO: we should probably update / refactor this


def executeInMayaStandalone(func: Callable) -> Callable:
    """
    Execute given function from standalone if possible

    :param func: callable a function to decorate

    :return: callable, decorated function

    """
    @wraps(func)
    def decor_func(*args, **kwargs) -> Callable:
        maya_standalone_init = False
        try:
            import maya.standalone
            maya.standalone.initialize()
            maya_standalone_init = True
        except RuntimeError:
            pass

        function_results = None

        try:
            function_results = func(*args, **kwargs)
        except Exception:
            cmds.warning(
                f"Exception found while running code on Maya Standalone : ")
            traceback.print_exc()

        finally:
            if maya_standalone_init:
                maya.standalone.uninitialize()

        return function_results

    return decor_func


def undoChunk(func: Callable) -> Callable:
    """
    Decorator to wrap a function in an undo chunk.

    :param func: callable a function to decorate

    :return: callable, decorated function

    """

    @wraps(func)
    def decor_func(*args, **kwargs) -> Callable:
        function_results = None
        cmds.undoInfo(openChunk=True)
        try:
            function_results = func(*args, **kwargs)
        except Exception:
            traceback.print_exc()
        finally:
            cmds.undoInfo(closeChunk=True)

        return function_results

    return decor_func


def timeIt(func: Callable):
    """
    A decorator to time the input function

    :param func: callable, a function to decorate

    :return: callable, decorated function

    """

    @wraps(func)
    def decor_func(*args, **kwargs) -> Callable:
        function_results = None

        print(f'\n[{func.__module__}.{func.__name__}] - START')

        start_timer = time.time()

        try:
            function_results = func(*args, **kwargs)

        except Exception as e:
            raise e

        finally:
            end_timer = time.time()
            print(
                f'\n[{func.__module__}.{func.__name__}] - '
                f'Took {end_timer - start_timer:.3f} seconds'
            )

        return function_results

    return decor_func


def getExecutionStats(func: Callable, sort_type: str = SortKey.CUMULATIVE):
    """
    Get detailed execution stats for the input function

    :param func: the function to get stats for
    :param sort_type: a key to format the output, see pstats.SortKey for more info

    :return: the result of the input function
    """

    @wraps(func)
    def decor_func(*args, **kwargs) -> Callable:
        profiler = cProfile.Profile()
        profiler.enable()  # start profiling

        function_results = func(*args, **kwargs)

        profiler.disable()  # stop profiling

        # Create stream for profile output
        stream = io.StringIO()
        ps = pstats.Stats(profiler, stream=stream)
        ps.sort_stats(sort_type)
        ps.print_stats(10)

        # print stream
        print(stream.getvalue())

        return function_results

    return decor_func
