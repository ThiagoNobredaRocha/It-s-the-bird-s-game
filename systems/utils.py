import math
from typing import Tuple


def dist(ax, ay, bx, by) -> float:
    return math.hypot(ax - bx, ay - by)


def normalize(vx, vy) -> Tuple[float, float]:
    mag = math.hypot(vx, vy)
    if mag == 0:
        return 0.0, 0.0
    return vx / mag, vy / mag


def lerp(a, b, t):
    return a + (b - a) * t


def clamp(v, lo, hi):
    return max(lo, min(hi, v))
