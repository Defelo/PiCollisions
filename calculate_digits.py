import sys
from decimal import Decimal

from physics import calculate_collision

if len(sys.argv) != 2 or not sys.argv[1].isnumeric() or int(sys.argv[1]) < 0:
    print(f"Usage: {sys.argv[0]} <digits>")
    exit()

m1: int = 1
m2: int = 100 ** int(sys.argv[1])
v1: Decimal = Decimal(0)
v2: Decimal = Decimal(-1)
x1: Decimal = Decimal(100)
x2: Decimal = Decimal(200)
w: int = 20
collisions: int = 0
wall: bool = False

# simulate until blocks cannot collide
while not (0 <= v1 <= v2):
    if wall:
        # left block collides with wall
        time_wall_collision: float = x1 / -v1
        x1 += time_wall_collision * v1
        x2 += time_wall_collision * v2
        v1 *= -1
    else:
        # blocks collide with each other
        time_block_collision: float = (w + x1 - x2) / (v2 - v1)
        x1 += time_block_collision * v1
        x2 += time_block_collision * v2
        v1, v2 = calculate_collision(m1, v1, m2, v2)
    collisions += 1
    wall = not wall

print(collisions)
