from .movement import MovementDirection, MovementActionType
import pygame
class TeacherRender:
    def __init__(self, teacher):
        self.teacher = teacher
        self.wait_time_start = 0
        self.teacher_is_walking = False

    def render(self, surface: pygame.Surface):
        if self.teacher.next_action is None:
            self.teacher.next_action = self.teacher.get_next_action()

        action_finished = False
        if self.teacher.next_action.action_type == MovementActionType.WALK:
            self.teacher.is_walking = True
            action_finished = self.animate_walk()
        if self.teacher.next_action.action_type == MovementActionType.WAIT:
            self.teacher.is_waiting = True
            action_finished = self.animate_wait()

        if action_finished:
            self.teacher.is_waiting = False
            self.teacher.is_walking = False
            self.teacher.next_action = self.teacher.get_next_action()

        self.render_sprite(surface)

    def render_sprite(self, surface: pygame.Surface):
        size_w = 60
        size_h = size_w / 2
        # body
        if self.teacher.next_action.direction in (MovementDirection.UP, MovementDirection.DOWN):
            pygame.draw.ellipse(surface, 'green', (self.teacher.current_grid_point_position.x - size_w / 2, self.teacher.current_grid_point_position.y - size_h / 2, size_w, size_h), 20)
        if self.teacher.next_action.direction in (MovementDirection.LEFT, MovementDirection.RIGHT):
            pygame.draw.ellipse(surface, 'green', (self.teacher.current_grid_point_position.x - size_h / 2, self.teacher.current_grid_point_position.y - size_w / 2, size_h, size_w), 20)
        #head
        pygame.draw.circle(surface, 'black', (self.teacher.current_grid_point_position.x, self.teacher.current_grid_point_position.y), 20)


    def animate_wait(self):
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
        