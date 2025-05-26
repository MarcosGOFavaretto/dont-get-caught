from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..render import GameRender
    from .student import Student
import pygame
from ..classroom.desk import ClassroomNpcDesk

class StudentRender:
    def __init__(self, game: 'GameRender', student: 'Student', surface: pygame.Surface):
        self.game = game
        self.student = student
        self.surface = surface

    def render(self):
        pygame.draw.rect(self.surface, 'brown', (self.student.position.x - ClassroomNpcDesk.width / 2, self.student.position.y - ClassroomNpcDesk.height / 2, ClassroomNpcDesk.width, ClassroomNpcDesk.height), 0)
        pygame.draw.rect(self.surface, 'brown', (self.student.position.x - 20, self.student.position.y + 26, 40, 10), 0)
        pygame.draw.ellipse(self.surface, 'red', (self.student.position.x - 20, self.student.position.y + 6, 40, 24), 20)
        pygame.draw.circle(self.surface, 'black', (self.student.position.x, self.student.position.y + 8), 14)