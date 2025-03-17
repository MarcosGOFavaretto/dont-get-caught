from ..classrooom.classroom import ClassroomGridPoint
from enum import Enum

class MovementDirection(Enum):
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    UP = 'UP'
    DOWN = 'DOWN'

class TeacherMovement:
    def __init__(self, point: ClassroomGridPoint, direction: MovementDirection):
        self.point = point
        self.direction = direction
        self.speed = 6

    def __str__(self):
        return f"TeacherMovement({self.point}, {self.direction})"