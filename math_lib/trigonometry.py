import math

from . import distance_between


__all__ = [
    'sin', 'cos', 'tan',
    'asin', 'acos', 'atan',
    'radians_to_degrees',
    'distances_to_radians',
    'distances_to_degrees',
    'points_to_radians',
    'points_to_degrees',
]


def sin(angle: float) -> float:

    """
    Sine of the given angle (radians)

    Args:
        angle: float, angle in radians

    Returns:
        float: sine of the angle
    """

    return math.sin(angle)


def cos(angle: float) -> float:

    """
    Cosine of the given angle

    Args:
        angle: float, angle in radians

    Returns:
        float: cosine of the angle
    """

    return math.cos(angle)


def tan(angle: float) -> float:

    """
    Tangent of the given angle

    Args:
        angle: float, angle in radians

    Returns:
        float: tangent of the angle
    """

    return math.tan(angle)


def asin(value: float) -> float:

    """
    Arc sine of the given value

    Args:
        value: float, value to run arc sine on

    Returns:
        float: arc sine of the value
    """

    return math.asin(value)


def acos(value: float) -> float:

    """
    Arc cosine of the given value

    Args:
        value: float, value to run arc cosine on

    Returns:
        float, arc cosine of the value
    """

    return math.acos(value)


def atan(value: float) -> float:

    """
    Retourne l'arc tangente de la valeur

    Args:
        value: float, value to run arc tangent on

    Returns:
        float, arc tangent of the value
    """

    return math.atan(value)


def radians_to_degrees(radians: float) -> float:

    """
    Convert radians to degrees

    Args:
        radians: float, radian value to convert

    Returns:
        float: degrees
    """

    return math.degrees(radians)


def distances_to_radians(dist_a: float, dist_b: float, dist_c: float) -> float:
    """
    Angle between three distances in radians

    Args:
        dist_a: float, Distance between a and b
        dist_b: float, Distance between b and c
        dist_c: float, Distance between a and c

    Returns:
        float: angle in radians
    """

    return math.acos(
        (dist_b**2 + dist_c**2 - dist_a**2) /
        (2 * dist_b * dist_c)
    )


def distances_to_degrees(dist_a: float, dist_b: float, dist_c: float) -> float:
    """
    Angle between three distances in degrees

    Args:
        dist_a: float, Distance between a and b
        dist_b: float, Distance between b and c
        dist_c: float, Distance between a and c

    Returns:
        float: angle in degrees
    """

    return radians_to_degrees(distances_to_radians(dist_a, dist_b, dist_c))


def points_to_radians(
    start_point: tuple[float, float, float],
    angle_point: tuple[float, float, float],
    end_point: tuple[float, float, float]
) -> float:

    """
    Angle between three points in radians

    Returns:
        float, angle in radians
    """

    dist_a = distance_between(start_point, angle_point)
    dist_b = distance_between(angle_point, end_point)
    dist_c = distance_between(start_point, end_point)

    return distances_to_radians(dist_a, dist_b, dist_c)


def points_to_degrees(
    start_point: tuple[float, float, float],
    angle_point: tuple[float, float, float],
    end_point: tuple[float, float, float]
) -> float:

    """
    Angle in degrees between three points

    Returns:
        float, angle in degrees
    """

    return radians_to_degrees(
        points_to_radians(
            start_point,
            angle_point,
            end_point
        )
    )
