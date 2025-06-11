from ast import PyCF_ALLOW_TOP_LEVEL_AWAIT
import math
from typing import TYPE_CHECKING
from ...timer import Timer, TIME_SECOND
if TYPE_CHECKING:
    from ..render import GameRender
    from .student import Student
import pygame
from ..classroom.desk import ClassroomNpcDesk
from ...utils import senoide

class StudentRender:
    def __init__(self, game: 'GameRender', student: 'Student', surface: pygame.Surface):
        self.game = game
        self.student = student
        self.surface = surface
        self.indicator_animation_timer = Timer(6 * TIME_SECOND)
        self.indicator_animation_timer.start()

    def render(self):
        pygame.draw.rect(self.surface, 'brown', (self.student.position.x - ClassroomNpcDesk.width / 2, self.student.position.y - ClassroomNpcDesk.height / 2, ClassroomNpcDesk.width, ClassroomNpcDesk.height), 0)
        pygame.draw.rect(self.surface, 'brown', (self.student.position.x - 20, self.student.position.y + 26, 40, 10), 0)
        pygame.draw.ellipse(self.surface, 'red', (self.student.position.x - 20, self.student.position.y + 6, 40, 24), 20)
        pygame.draw.circle(self.surface, 'black', (self.student.position.x, self.student.position.y + 8), 14)

        if not self.indicator_animation_timer.time_is_up():
            self.render_player_indicator()
        
    def render_player_indicator(self):
        animation_amplitude = senoide(10, 1/1000, 0, 0, self.indicator_animation_timer.get_time_passed()) + 40
        indicator_y = animation_amplitude
        indicator_size = 8
        pygame.draw.polygon(self.surface, 'red', [
            (self.student.position.x - indicator_size, self.student.position.y - indicator_y), 
            (self.student.position.x, self.student.position.y - indicator_y + indicator_size), 
            (self.student.position.x + indicator_size, self.student.position.y - indicator_y)])
        