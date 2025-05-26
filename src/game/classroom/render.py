import pygame
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .classroom import Classroom
    from ..render import GameRender

class ClassroomRender:
    def __init__(self, game: 'GameRender', classroom: 'Classroom', surface: pygame.Surface):
        self.game = game
        self.classroom = classroom
        self.surface = surface
        
    def render(self):
        for row in self.classroom.grid_points:
            for point in row:
                desk_is_player = (self.game.student.position.column, self.game.student.position.row) == (point.column, point.row)
                if point.classroom_desk is not None and not desk_is_player:
                    pygame.draw.rect(self.surface, 'brown', (point.x - point.classroom_desk.width / 2, point.y - point.classroom_desk.height / 2, point.classroom_desk.width, point.classroom_desk.height), 0)
                    if point.classroom_desk.has_student:
                        pygame.draw.rect(self.surface, 'brown', (point.x - 20, point.y + 26, 40, 10), 0)
                        pygame.draw.ellipse(self.surface, 'blue', (point.x - 20, point.y + 6, 40, 24), 20)
                        pygame.draw.circle(self.surface, 'black', (point.x, point.y + 8), 14)