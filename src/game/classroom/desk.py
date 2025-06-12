from typing import TYPE_CHECKING

import pygame
if TYPE_CHECKING:
    from .grid import ClassroomGridPoint

class ClassroomNpcDesk:
    width = 60
    height = width - 20
    def __init__(self, grid_position: 'ClassroomGridPoint', sprite: pygame.Surface, has_student: bool = False):
        self.grid_position = grid_position
        self.has_student = has_student
        self.sprite = sprite
        
