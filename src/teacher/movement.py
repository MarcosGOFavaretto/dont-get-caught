from ..classrooom.classroom import ClassroomGridPoint
from enum import Enum

class MovementDirection(Enum):
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    UP = 'UP'
    DOWN = 'DOWN'

class MovementActionType(Enum):
    WALK = 'WALK'
    STAND = 'STAND'


class MovementAction:
    def __init__(self, action_type: MovementActionType, point: ClassroomGridPoint, direction: MovementDirection):
        self.action_type = action_type
        self.direction = direction
        self.point = point

class MovementActionWalk(MovementAction):
    def __init__(self, point: ClassroomGridPoint, direction: MovementDirection, speed: float):
        super().__init__(MovementActionType.WALK, point, direction)
        self.speed = speed

class MovementActionStand(MovementAction):
    def __init__(self, point: ClassroomGridPoint, direction: MovementDirection, wait: float):
        super().__init__(MovementActionType.STAND, point, direction)
        self.wait = wait

class TeacherAction:
    def __init__(self, action: MovementAction):
        self.action: MovementAction = action

    def __str__(self):
        return f"TeacherMovement({self.point}, {self.direction})"