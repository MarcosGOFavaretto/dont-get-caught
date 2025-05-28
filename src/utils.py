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

def senoide(max_amplitude: float, frequency: float, offset_x: float, offset_y: float, square_shapping: float, time: float):
    w = 2 * math.pi * frequency
    max_amplitude *= 1 + square_shapping 
    wave = math.sin(w * time + offset_x)
    return max_amplitude * (wave/(abs(wave) + square_shapping)) + offset_y

def circular(center_x: float, center_y: float, radius: float, velocity: float, offset: float, time: float):
    x = center_x + radius * math.cos(time * velocity + offset)
    y = center_y + radius * math.sin(time * velocity + offset)
    return (x, y)

def triangle_senoide(max_amplitude: float, frequency: float, offset_x: float, offset_y: float, time: float):
    w = 2 * math.pi * frequency
    return max_amplitude * 2 / math.pi * math.asin(math.sin(w * time + offset_x)) + offset_y