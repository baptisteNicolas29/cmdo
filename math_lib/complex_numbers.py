from typing import Optional, List

import math


__all__ = [
    'euler_to_quaternions',
    'quaternions_to_euler',
    'normalize_quaternion'
]


def euler_to_quaternions(
    roll: Optional[float] = 0.0,
    pitch: Optional[float] = 0.0,
    yaw: Optional[float] = 0.0,
) -> List[float]:
    """
    Convert euler angle to quaternion

    :param Optional[float] roll: The roll (x) angle.
    :param Optional[float] pitch: The pitch (y) angle.
    :param Optional[float] yaw: The yaw (z) angle.
    :return: the quaternion
    """

    angles = {"roll": roll, "pitch": pitch, "yaw": yaw}
    angles = {angle: math.radians(value) for angle, value in angles.items()}

    cr = math.cos(angles["roll"] * 0.5)
    sr = math.sin(angles["roll"] * 0.5)
    cp = math.cos(angles["pitch"] * 0.5)
    sp = math.sin(angles["pitch"] * 0.5)
    cy = math.cos(angles["yaw"] * 0.5)
    sy = math.sin(angles["yaw"] * 0.5)

    qw = cr * cp * cy + sr * sp * sy
    qx = sr * cp * cy - cr * sp * sy
    qy = cr * sp * cy + sr * cp * sy
    qz = cr * cp * sy - sr * sp * cy

    return [qx, qy, qz, qw]


def quaternions_to_euler(
        qx: Optional[float] = 0.0,
        qy: Optional[float] = 0.0,
        qz: Optional[float] = 0.0,
        qw: Optional[float] = 1.0
) -> List[float]:
    """
    Convert quaternion to euler

    :param Optional[float] qx: the x value of the quaternion
    :param Optional[float] qy: the y value of the quaternion
    :param Optional[float] qz: the z value of the quaternion
    :param Optional[float] qw: the w value of the quaternion
    :return: xyz values in degrees
    """
    x, y, z, w = normalize_quaternion(qx, qy, qz, qw)

    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x ** 2 + y ** 2)
    roll = math.atan2(sinr_cosp, cosr_cosp)

    sinp = math.sqrt(1 + 2 * (w * y + x * z))
    cosp = math.sqrt(1 - 2 * (w * y - x * z))
    pitch = 2 * math.atan2(sinp, cosp) - math.pi / 2

    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y ** 2 + z ** 2)
    yaw = math.atan2(siny_cosp, cosy_cosp)

    return [math.degrees(roll), math.degrees(pitch), math.degrees(yaw)]


def normalize_quaternion(
        qx: Optional[float] = 0.0,
        qy: Optional[float] = 0.0,
        qz: Optional[float] = 0.0,
        qw: Optional[float] = 1.0
) -> List[float]:
    """
    Normalize the given quaternion

    :param Optional[float] qx: the x value of the quaternion
    :param Optional[float] qy: the y value of the quaternion
    :param Optional[float] qz: the z value of the quaternion
    :param Optional[float] qw: the w value of the quaternion
    :return: the normalized quaternion
    """
    # need to have default to 1.0 to avoid division by zero
    norm_magnitude = math.sqrt(qx ** 2 + qy ** 2 + qz ** 2 + qw ** 2) or 1.0

    x = qx / norm_magnitude
    y = qy / norm_magnitude
    z = qz / norm_magnitude
    w = qw / norm_magnitude

    return [x, y, z, w]
