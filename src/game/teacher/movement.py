from ..classroom.classroom import ClassroomGridPoint
from enum import Enum
import pygame
import copy

class MovementDirection(Enum):
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    UP = 'UP'
    DOWN = 'DOWN'

    def get_directions_rotation_map(self):
        directions = None
        if self == MovementDirection.LEFT:
            directions = (0, 3, 2, 1)
        elif self == MovementDirection.UP:
            directions = (1, 0, 3, 2)
        elif self == MovementDirection.RIGHT:
            directions = (2, 1, 0, 3)
        elif self == MovementDirection.DOWN:
            directions = (3, 2, 1, 0)
        else:
            raise ValueError("Invalid direction")
        return {
            MovementDirection.LEFT: directions[0] * 90,
            MovementDirection.UP: directions[1] * 90,
            MovementDirection.RIGHT: directions[2] * 90,
            MovementDirection.DOWN: directions[3] * 90
        }

    # def get_left_rotation(self):
    #     if self == MovementDirection.LEFT:
    #         return 0
    #     elif self == MovementDirection.RIGHT:
    #         return -180
    #     elif self == MovementDirection.UP:
    #         return -90
    #     elif self == MovementDirection.DOWN:
    #         return 90
    #     else:
    #         raise ValueError("Invalid direction")
        
    # def get_up_rotation(self):
    #     if self == MovementDirection.LEFT:
    #         return 90
    #     elif self == MovementDirection.RIGHT:
    #         return -90
    #     elif self == MovementDirection.UP:
    #         return 0
    #     elif self == MovementDirection.DOWN:
    #         return 90
    #     else:
    #         raise ValueError("Invalid direction")

class MovementActionType(Enum):
    WALK = 'WALK'
    WAIT = 'WAIT'

class MovementAction:
    def __init__(self, action_type: MovementActionType, final_point: ClassroomGridPoint, direction: MovementDirection):
        self.action_type = action_type
        self.direction = direction
        self.final_point = final_point

class MovementActionWalk(MovementAction):
    def __init__(self, current_point: ClassroomGridPoint, final_point: ClassroomGridPoint, walk_speed: float, walk_path: list[ClassroomGridPoint]):
        self.walk_path = walk_path
        self.path_cursor = 0
        self.next_point: ClassroomGridPoint | None = copy.deepcopy(self.walk_path[self.path_cursor])
        self.current_point = current_point
        self.walk_speed = walk_speed
        self.direction = self.get_walk_direction()
        super().__init__(MovementActionType.WALK, final_point, self.direction)

    def advance_path(self):
        self.path_cursor += 1
        if self.path_cursor >= len(self.walk_path):
            self.next_point = None
            return 
        if self.next_point:
            self.current_point = self.next_point
        self.next_point = copy.deepcopy(self.walk_path[self.path_cursor])
        self.direction = self.get_walk_direction()
    
    def get_walk_direction(self):
        if self.next_point is None:
            raise ValueError("Next point is None, cannot set direction.")
        if self.current_point.row < self.next_point.row:
            return MovementDirection.DOWN
        elif self.current_point.row > self.next_point.row:
            return MovementDirection.UP
        elif self.current_point.column < self.next_point.column:
            return MovementDirection.RIGHT
        elif self.current_point.column > self.next_point.column:
            return MovementDirection.LEFT
        else:
            raise ValueError("Current point and next point are the same, cannot set direction.")
    
    
class MovementActionWait(MovementAction):
    def __init__(self, point: ClassroomGridPoint, direction_to_look: MovementDirection, wait_time: float):
        super().__init__(MovementActionType.WAIT, point, direction_to_look)
        self.wait_time = wait_time
        self.wait_time_start = 0

    def start_timer(self):
        self.wait_time_start = pygame.time.get_ticks()    

    def get_time_passed(self):
        return pygame.time.get_ticks() - self.wait_time_start
