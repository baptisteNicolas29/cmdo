from typing import List, Union

# import math
# import numpy

from maya.api import OpenMaya as om


__all__ = [
    'identityMatrix4',
    'isSameLengthMatrix',
    'isIdentityMatrix4',
    'isAlmostSameMatrix',
    'multiplyMatrices',
]


identityMatrix4 = [
    1.0 if col == row else 0.0
    for col in range(4)
    for row in range(4)
]


def isSameLengthMatrix(mtx1: List[Union[int, float]], mtx2: List[Union[int, float]]) -> bool:
    """
    Checks if both input matrices are the same length

    Args:
        mtx1: matrix to compare the length of
        mtx2: matrix to compare the length of

    Returns:
        if the matrices are the same length
    """
    return len(mtx1) == len(mtx2)


def isIdentityMatrix4(mtx1: List[Union[int, float]],  epsilon: float = 0.0001) -> bool:
    """
    Checks if the input matrix is close to the 4x4 identity

    Args:
        mtx1: the input matrix to check
        epsilon: the precision for floating point numbers

    Returns:
        if the matrix is and identity matrix
    """

    return isAlmostSameMatrix(mtx1, identityMatrix4, epsilon=epsilon)


def isAlmostSameMatrix(
    mtx1: List[Union[int, float]],
    mtx2: List[Union[int, float]],
    epsilon: float = 0.0001
) -> bool:
    """
    Check if two matrices are really close to each other
    Due to floating point precision, we can t check equality
    Args:
        mtx1: matrix to compare
        mtx2: matrix to compare
        epsilon: the precision for floating point numbers

    Returns:
        if the matrices are almost the same given epsilon
    """
    return (
        isSameLengthMatrix(mtx1, mtx2) and
        all(abs(x1 - x2) < epsilon for x1, x2 in zip(mtx1, mtx2))
    )


def multiplyMatrices(mtx1: List[Union[int, float]], mtx2: List[Union[int, float]]):
    print(f'{len(mtx1)=} x {len(mtx2)=}')

    if not isSameLengthMatrix(mtx1, mtx2):
        raise Exception('Cannot multiply matrices of different lengths')

    return om.MMatrix(mtx1) * om.MMatrix(mtx2)
