import pygame

class ClassroomRender:
    def __init__(self, classroom, surface: pygame.Surface):
        self.classroom = classroom
        self.surface = surface


    def render(self):
        # Desenha cada ponto do grid da sala
        # Se o ponto for uma carteira, desenha uma carteira
        for row in self.classroom.grid_points:
            for point in row:
                if point.is_student_desk:
                    pygame.draw.rect(self.surface, 'brown', (point.x - self.classroom.desk_width / 2, point.y - self.classroom.desk_height / 2, self.classroom.desk_width, self.classroom.desk_height), 0)
            #     continue
            # pygame.draw.circle(surface, 'red', (point.x, point.y), 5)