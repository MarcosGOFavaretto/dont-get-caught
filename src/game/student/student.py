from ..classroom.grid import ClassroomGridPoint
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..render import GameRender
from .render import StudentRender
import pygame
import copy

class Student:
    def __init__(self, game: 'GameRender', position: ClassroomGridPoint):
        self.position = position
        self.game = game
        self.hearing_teacher_steps_range = 800

    def get_render(self, surface: pygame.Surface):
        return StudentRender(self.game, self, surface)
    
    def get_neighbor_grid_points(self):
        x, y = self.position.column, self.position.row
        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        return [copy.deepcopy(self.game.classroom.grid_points[nx][ny]) for nx, ny in neighbors if 0 <= nx < self.game.classroom.grid_columns and 0 <= ny < self.game.classroom.grid_rows]