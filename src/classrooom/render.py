import pygame

class ClassroomRender:
    def __init__(self, classroom):
        self.classroom = classroom

    def render(self, surface: pygame.Surface):
        # Desenha cada ponto do grid da sala
        # Se o ponto for uma carteira, desenha uma carteira
        for point in self.classroom.grid_points:
            if point.is_student_desk:
                pygame.draw.circle(surface, 'brown', (point.x , point.y), 16)
                continue
            pygame.draw.circle(surface, 'red', (point.x, point.y), 5)