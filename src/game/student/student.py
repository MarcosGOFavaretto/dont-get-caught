from ..classroom.grid import ClassroomGridPoint

class Student:
    def __init__(self, game: any, position: ClassroomGridPoint):
        self.position = position
        self.game = game
        self.hearing_teacher_steps_range = 1000