from .desk import ClassroomNpcDesk
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .classroom import Classroom

class ClassroomGridPoint:
    def __init__(self, column: int, row: int, x: int, y: int, classroom_desk: ClassroomNpcDesk | None):
        self.column = column
        self.row = row
        self.classroom_desk = classroom_desk
        self.x = x
        self.y = y

    def __eq__(self, value):
        return value.column == self.column and value.row == self.row
    
    def to_grid_point(self): 
        return (self.column, self.row)
    
    def to_coordenate(self): 
        return (self.x, self.y)