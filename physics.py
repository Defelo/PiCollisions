from typing import Tuple


def calculate_collision(m1: float, v1: float, m2: float, v2: float) -> Tuple[float, float]:
    """
    Calculates the new velocities after the two blocks collide.

    :param m1: Mass of first block
    :param v1: Velocity of first block
    :param m2: Mass of second block
    :param v2: Velocity of second block
    :return: The two new velocities
    """

    mv: float = m1 * v1 + m2 * v2
    s: float = m1 + m2
    b: float = mv / s
    d: float = (b ** 2 - (mv ** 2 - (m1 * v1 ** 2 + m2 * v2 ** 2) * m2) / (m1 * s)) ** .5
    new_v1: float = max([b - d, b + d], key=lambda a: abs(a - v1))
    d: float = (b ** 2 - (mv ** 2 - (m1 * v1 ** 2 + m2 * v2 ** 2) * m1) / (m2 * s)) ** .5
    new_v2: float = max([b - d, b + d], key=lambda a: abs(a - v2))
    return new_v1, new_v2
