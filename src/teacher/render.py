from .movement import MovementDirection, MovementActionType
import pygame
class TeacherRender:
    def __init__(self, teacher):
        self.teacher = teacher
        self.wait_time_start = 0


    def render(self, surface: pygame.Surface):
        if self.teacher.next_action is None:
            self.teacher.next_action = self.teacher.get_next_action()

        action_finished = False
        if self.teacher.next_action.action_type == MovementActionType.WALK:
            action_finished = self.animate_walk()
        if self.teacher.next_action.action_type == MovementActionType.STAND:
            action_finished = self.animate_stand()

        pygame.draw.circle(surface, 'green', (self.teacher.current_grid_point_position.x, self.teacher.current_grid_point_position.y), 20)

        if action_finished:
            self.teacher.next_action = self.teacher.get_next_action()

    def animate_stand(self):
        if self.wait_time_start == 0:
            self.wait_time_start = pygame.time.get_ticks()
            
        if (pygame.time.get_ticks() - self.wait_time_start) >= self.teacher.next_action.wait:
            self.wait_time_start = 0
            return True

        return False

    def animate_walk(self):
        # Verifica se o professor terminou a ação
        is_end_point = False
        if self.teacher.next_action.direction == MovementDirection.LEFT:
            is_end_point = self.teacher.current_grid_point_position.x <= self.teacher.next_action.point.x and self.teacher.current_grid_point_position.y == self.teacher.next_action.point.y
        if self.teacher.next_action.direction == MovementDirection.RIGHT:
            is_end_point = self.teacher.current_grid_point_position.x >= self.teacher.next_action.point.x and self.teacher.current_grid_point_position.y == self.teacher.next_action.point.y
        if self.teacher.next_action.direction == MovementDirection.UP:
            is_end_point = self.teacher.current_grid_point_position.x == self.teacher.next_action.point.x and self.teacher.current_grid_point_position.y <= self.teacher.next_action.point.y
        if self.teacher.next_action.direction == MovementDirection.DOWN:
            is_end_point = self.teacher.current_grid_point_position.x == self.teacher.next_action.point.x and self.teacher.current_grid_point_position.y >= self.teacher.next_action.point.y

        # Muda os pontos de coordenada para movimentar o professor.
        if not is_end_point:
            if self.teacher.next_action.direction == MovementDirection.LEFT:
                self.teacher.current_grid_point_position.x -= self.teacher.next_action.speed
            if self.teacher.next_action.direction == MovementDirection.RIGHT:
                self.teacher.current_grid_point_position.x += self.teacher.next_action.speed
            if self.teacher.next_action.direction == MovementDirection.UP:
                self.teacher.current_grid_point_position.y -= self.teacher.next_action.speed
            if self.teacher.next_action.direction == MovementDirection.DOWN:
                self.teacher.current_grid_point_position.y += self.teacher.next_action.speed
            return False
        
        self.teacher.current_grid_point_position = self.teacher.classroom.create_grid_point(self.teacher.next_action.point.row, self.teacher.next_action.point.column)

        return True
        