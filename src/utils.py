import math

def get_angle_between_points(a :tuple[float, float], b: tuple[float, float]) -> float:
    dist_x = a[0] - b[0]
    dist_y = - a[1] + b[1]
    angle = math.degrees(math.atan2(dist_y, dist_x)) % 360
    return angle

def heuristic(a: tuple[int, int], b: tuple[int, int]) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def map_value(value: float, in_min: float, in_max: float, out_min: float, out_max: float) -> float:
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min