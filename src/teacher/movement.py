from ..classrooom.classroom import ClassroomGridPoint
from enum import Enum

class MovementDirection(Enum):
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    UP = 'UP'
    DOWN = 'DOWN'

class MovementActionType(Enum):
    WALK = 'WALK'
    WAIT = 'WAIT'


class MovementAction:
    def __init__(self, action_type: MovementActionType, point: ClassroomGridPoint, direction: MovementDirection):
        self.action_type = action_type
        self.direction = direction
        self.point = point

class MovementActionWalk(MovementAction):
    def __init__(self, point: ClassroomGridPoint, direction: MovementDirection, speed: float):
        super().__init__(MovementActionType.WALK, point, direction)
        self.speed = speed

class MovementActionWait(MovementAction):
    def __init__(self, point: ClassroomGridPoint, direction: MovementDirection, wait_time: float):
        super().__init__(MovementActionType.WAIT, point, direction)
        self.wait_time = wait_time