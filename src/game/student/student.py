from ..classroom.grid import ClassroomGridPoint
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..render import GameRender

class Student:
    def __init__(self, game: 'GameRender', position: ClassroomGridPoint):
        self.position = position
        self.game = game
        self.hearing_teacher_steps_range = 500