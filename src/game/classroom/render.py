import pygame

class ClassroomRender:
    def __init__(self, classroom, surface: pygame.Surface):
        self.classroom = classroom
        self.surface = surface
        
    def render(self):
        for row in self.classroom.grid_points:
            for point in row:
                if point.is_student_desk:
                    pygame.draw.rect(self.surface, 'brown', (point.x - self.classroom.desk_width / 2, point.y - self.classroom.desk_height / 2, self.classroom.desk_width, self.classroom.desk_height), 0)