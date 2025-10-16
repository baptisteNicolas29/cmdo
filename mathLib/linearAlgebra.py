from typing import Tuple, List

import math


__all__: List[str] = [
    'distance_between',
]


def distance_between(
    point1: Tuple[float, float, float],
    point2: Tuple[float, float, float]
) -> float:

    """
    Retourne la distance entre deux points

    Args:
        point1 (Tuple[float, float, float]):
            Premier point
        point2 (Tuple[float, float, float]):
            Deuxième point

    Returns:
        float: distance entre les deux points
    """

    return math.sqrt(
        (point2[0] - point1[0]) ** 2 +
        (point2[1] - point1[1]) ** 2 +
        (point2[2] - point1[2]) ** 2
    )
