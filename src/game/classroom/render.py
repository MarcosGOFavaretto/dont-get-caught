import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .classroom import Classroom
    from ..render import GameRender
from ...config import WINDOW_WIDTH, WINDOW_HEIGHT, ASSETS_FOLDER
import os
import random

class ClassroomRender:
    def __init__(self, game: 'GameRender', classroom: 'Classroom'):
        self.game = game
        self.surface = game.app.surface
        self.classroom = classroom
        self.floor_sprite = pygame.image.load(f'{ASSETS_FOLDER}/images/classroom-floor.png')
        self.desk_without_student_sprite = pygame.image.load(f'{ASSETS_FOLDER}/images/desk-without-student.png')
        
    def render(self):
        self.render_floor()
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
                if point.classroom_desk.has_student:
                    self.surface.blit(point.classroom_desk.sprite, (point.x - 32, point.y - 32))
                else:
                    self.surface.blit(self.desk_without_student_sprite, (point.x - 32, point.y - 32))

    
    def render_floor(self):
        for x in range(0, WINDOW_WIDTH, 64):
            for y in range(0, WINDOW_HEIGHT + self.game.animation_classroom_offset, 64):
                self.surface.blit(self.floor_sprite, (x, self.classroom.y + y - self.game.animation_classroom_offset))


    def get_random_npc_student(self):
        return random.choice(os.listdir(f'{ASSETS_FOLDER}/npc_students'))