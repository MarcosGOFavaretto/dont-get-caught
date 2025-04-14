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
                    desk_w = 60
                    desk_h = desk_w - 20
                    pygame.draw.rect(self.surface, 'brown', (point.x - desk_w / 2, point.y - desk_h / 2, desk_w, desk_h), 0)
            #     continue
            # pygame.draw.circle(surface, 'red', (point.x, point.y), 5)