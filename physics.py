from decimal import Decimal
from typing import Tuple


def calculate_collision(m1: int, v1: Decimal, m2: int, v2: Decimal) -> Tuple[Decimal, Decimal]:
    """
    Calculates the new velocities after the two blocks collide.

    :param m1: Mass of first block
    :param v1: Velocity of first block
    :param m2: Mass of second block
    :param v2: Velocity of second block
    :return: The two new velocities
    """

    mv: Decimal = m1 * v1 + m2 * v2
    s: Decimal = m1 + m2
    b: Decimal = mv / s
    d: Decimal = (b ** 2 - (mv ** 2 - (m1 * v1 ** 2 + m2 * v2 ** 2) * m2) / (m1 * s)).sqrt()
    new_v1: Decimal = max([b - d, b + d], key=lambda a: abs(a - v1))
    d: Decimal = (b ** 2 - (mv ** 2 - (m1 * v1 ** 2 + m2 * v2 ** 2) * m1) / (m2 * s)).sqrt()
    new_v2: Decimal = max([b - d, b + d], key=lambda a: abs(a - v2))
    return new_v1, new_v2
