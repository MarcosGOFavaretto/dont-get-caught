from ast import PyCF_ALLOW_TOP_LEVEL_AWAIT
from typing import TYPE_CHECKING
from ...timer import Timer, TIME_SECOND
if TYPE_CHECKING:
    from ..render import GameRender
    from .student import Student
import pygame
from ..classroom.desk import ClassroomNpcDesk
from ...utils import senoide
from ...config import ASSETS_FOLDER

class StudentRender:
    def __init__(self, game: 'GameRender', student: 'Student', surface: pygame.Surface):
        self.game = game
        self.student = student
        self.surface = surface
        self.indicator_animation_timer = Timer(6 * TIME_SECOND)
        self.indicator_animation_timer.start()
        self.student_player_sprite = pygame.image.load(f'{ASSETS_FOLDER}/student-player.png')
        self.player_indicator_sprite = pygame.image.load(f'{ASSETS_FOLDER}/player-indicator.png')

    def render(self):
        self.surface.blit(self.student_player_sprite, (self.student.position.x - 32, self.student.position.y - 32))
        if not self.indicator_animation_timer.time_is_up():
            self.render_player_indicator()
        
    def render_player_indicator(self):
        animation_amplitude = senoide(10, 1/1000, 0, 0, self.indicator_animation_timer.get_time_passed()) + 40
        indicator_y = animation_amplitude
        self.surface.blit(self.player_indicator_sprite, (self.student.position.x - 32, self.student.position.y - 32 - indicator_y))
        