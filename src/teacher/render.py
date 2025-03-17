from .movement import MovementDirection
import pygame

class TeacherRender:
    def __init__(self, teacher):
        self.teacher = teacher

    def render(self, surface: pygame.Surface):
        if self.teacher.next_mv is None:
            self.teacher.next_mv = self.teacher.next_movement()

        # Verifica se o professor terminou a ação
        is_end_point = False
        if self.teacher.next_mv.direction == MovementDirection.LEFT:
            is_end_point = self.teacher.current_grid_point_position.x <= self.teacher.next_mv.point.x and self.teacher.current_grid_point_position.y == self.teacher.next_mv.point.y
        if self.teacher.next_mv.direction == MovementDirection.RIGHT:
            is_end_point = self.teacher.current_grid_point_position.x >= self.teacher.next_mv.point.x and self.teacher.current_grid_point_position.y == self.teacher.next_mv.point.y
        if self.teacher.next_mv.direction == MovementDirection.UP:
            is_end_point = self.teacher.current_grid_point_position.x == self.teacher.next_mv.point.x and self.teacher.current_grid_point_position.y <= self.teacher.next_mv.point.y
        if self.teacher.next_mv.direction == MovementDirection.DOWN:
            is_end_point = self.teacher.current_grid_point_position.x == self.teacher.next_mv.point.x and self.teacher.current_grid_point_position.y >= self.teacher.next_mv.point.y

        # Muda os pontos de coordenada para movimentar o professor.
        if not is_end_point:
            if self.teacher.next_mv.direction == MovementDirection.LEFT:
                self.teacher.current_grid_point_position.x -= self.teacher.next_mv.speed
            if self.teacher.next_mv.direction == MovementDirection.RIGHT:
                self.teacher.current_grid_point_position.x += self.teacher.next_mv.speed
            if self.teacher.next_mv.direction == MovementDirection.UP:
                self.teacher.current_grid_point_position.y -= self.teacher.next_mv.speed
            if self.teacher.next_mv.direction == MovementDirection.DOWN:
                self.teacher.current_grid_point_position.y += self.teacher.next_mv.speed
        else:
            # Quando o professor terminar de executar a ação uma nova ação é criada.
            self.teacher.current_grid_point_position = self.teacher.classroom.create_grid_point(self.teacher.next_mv.point.row, self.teacher.next_mv.point.column)
            self.teacher.next_mv = self.teacher.next_movement()
            
        pygame.draw.circle(surface, 'green', (self.teacher.current_grid_point_position.x, self.teacher.current_grid_point_position.y), 20)