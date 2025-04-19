import math

def get_angle_between_points(a :tuple[float, float], b: tuple[float, float]) -> float:
    dist_x = a[0] - b[0]
    dist_y = - a[1] + b[1]
    angle = math.degrees(math.atan2(dist_y, dist_x)) % 360
    return angle