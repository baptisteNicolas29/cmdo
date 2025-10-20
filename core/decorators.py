import io
import time
import numpy
import pstats
import cProfile
import traceback
from pstats import SortKey
from functools import wraps

from maya import cmds


# TODO: probably remove / rework all of this


def execute_in_maya_standalone(func: callable) -> callable:
    """
    Execute given function from standalone if possible

    Args:
        func:

    Returns:

    """
    @wraps(func)
    def decor_func(*args, **kwargs) -> callable:
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


def undo_chunk(func: callable) -> callable:
    """
    Decorator to wrap a function in an undo chunk.

    Returns: the result of the input function
    """

    @wraps(func)
    def decor_func(*args, **kwargs) -> callable:
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


def time_it(func: callable):
    """
    A decorator to time the input function

    Args:
        func: a function to time

    Returns:
        the results of the function
    """
    @wraps(func)
    def decor_func(*args, **kwargs) -> callable:
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


def get_execution_stats(func: callable, sort_type: str = SortKey.CUMULATIVE):
    """
    Get detailed execution stats for the input function

    Args:
        func: the function to get stats for
        sort_type: a key to format the output, see pstats.SortKey for more info

    Returns:
        the result of the input function
    """
    @wraps(func)
    def decor_func(*args, **kwargs) -> callable:
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


def vectorize_function(func: callable):
    """
    A decorator to vectorize a function using numpy
    Numpy vectorization is used to apply a function to every element of
    an iterable at the same time

    Args:
        func: a function to vectorize

    Returns:
        the results of the function
    """
    @wraps(func)
    def decor_func(*args, **kwargs) -> callable:

        try:
            np_func = numpy.vectorize(func)
            function_results = np_func(*args, **kwargs)

        except Exception as e:
            raise e

        return function_results

    return decor_func


def raise_on_exception(func):

    @wraps(func)
    def decor_func(*args, **kwargs) -> callable:

        try:
            function_results = func(*args, **kwargs)

        except Exception as e:

            raise Exception('Raise from decorator') from e

        return function_results

    return decor_func
