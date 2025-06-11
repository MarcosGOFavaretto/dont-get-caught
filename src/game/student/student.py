from ..classroom.grid import ClassroomGridPoint
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..render import GameRender
from .render import StudentRender
import pygame

class Student:
    def __init__(self, game: 'GameRender', position: ClassroomGridPoint):
        self.position = position
        self.game = game
        self.hearing_teacher_steps_range = 800

    def get_render(self, surface: pygame.Surface):
        return StudentRender(self.game, self, surface)