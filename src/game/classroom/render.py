import pygame
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .classroom import Classroom
    from ..render import GameRender
from ...config import WINDOW_WIDTH

class ClassroomRender:
    def __init__(self, game: 'GameRender', classroom: 'Classroom', surface: pygame.Surface):
        self.game = game
        self.classroom = classroom
        self.surface = surface
        
    def render(self):
        self.render_desks()

        if not self.game.started:
            # Lousa
            self.render_chalkboard()
            # Porta
            self.render_door()
            # Mesa do professor
            self.render_teacher_desk()

    def render_teacher_desk(self):
        desk_width = 200
        walk_dist = 40
        pygame.draw.rect(self.surface, 'brown', (WINDOW_WIDTH - desk_width - walk_dist, 80 - self.game.animation_control, desk_width, 100), 0)
        chair_width = 60
        pygame.draw.rect(self.surface, 'brown', (WINDOW_WIDTH - walk_dist - desk_width // 2 - chair_width // 2, 20 - self.game.animation_control, chair_width, 10), 0)
        pygame.draw.rect(self.surface, 'brown', (WINDOW_WIDTH - walk_dist - desk_width // 2 - (chair_width - 10) // 2, 20 - self.game.animation_control, (chair_width - 10), 40), 0)

    def render_chalkboard(self):
        chalboard_width = 500
        chalboard_height = 10
        pygame.draw.rect(self.surface, 'black', (WINDOW_WIDTH // 2 - chalboard_width // 2, 0 - self.game.animation_control, chalboard_width, chalboard_height), 0)
        giz_bar_width = 480
        pygame.draw.rect(self.surface, 'white', (WINDOW_WIDTH // 2 - giz_bar_width // 2, chalboard_height - self.game.animation_control, giz_bar_width, 14), 0)

    def render_door(self):
        pygame.draw.line(self.surface, 'brown', (-10, 100 - self.game.animation_control), (50, 50 - self.game.animation_control), 8)

    def render_desks(self):
        for point in self.classroom.get_grid_points_list():
            desk_is_player = (self.game.student.position.column, self.game.student.position.row) == (point.column, point.row)
            if point.classroom_desk is not None and not desk_is_player:
                pygame.draw.rect(self.surface, 'brown', (point.x - point.classroom_desk.width / 2, point.y - point.classroom_desk.height / 2, point.classroom_desk.width, point.classroom_desk.height), 0)
                if point.classroom_desk.has_student:
                    pygame.draw.rect(self.surface, 'brown', (point.x - 20, point.y + 26, 40, 10), 0)
                    pygame.draw.ellipse(self.surface, 'blue', (point.x - 20, point.y + 6, 40, 24), 20)
                    pygame.draw.circle(self.surface, 'black', (point.x, point.y + 8), 14)
