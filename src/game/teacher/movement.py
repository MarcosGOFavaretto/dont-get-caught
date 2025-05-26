from ..classroom.classroom import ClassroomGridPoint, Classroom
from enum import Enum
import pygame
import copy

class MovementDirection(Enum):
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    UP = 'UP'
    DOWN = 'DOWN'

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
