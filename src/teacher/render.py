from .movement import MovementDirection, MovementActionType
import pygame
from ..classrooom.grid import ClassroomGridPoint
class TeacherRender:
    def __init__(self, teacher):
        self.teacher = teacher

    def render(self, surface: pygame.Surface):
        if self.teacher.current_action is None:
            self.next_action()

        if self.teacher.current_action.action_type == MovementActionType.WALK:
            self.teacher.is_walking = True
            self.animate_walk()
        elif self.teacher.current_action.action_type == MovementActionType.WAIT:
            self.teacher.is_waiting = True
            self.animate_wait()

        self.render_sprite(surface)

    def next_action(self):
        self.teacher.is_waiting = False
        self.teacher.is_walking = False
        self.teacher.current_action = self.teacher.get_next_action()
    
    def animate_walk(self):
        walk_direction = self.teacher.current_action.direction
        self.teacher.direction = walk_direction

        # Verifica se o professor terminou o passo
        is_next_point = False
        if walk_direction == MovementDirection.LEFT:
            is_next_point = self.teacher.current_grid_point_position.x <= self.teacher.current_action.next_point.x and self.teacher.current_grid_point_position.y == self.teacher.current_action.next_point.y
        elif walk_direction == MovementDirection.RIGHT:
            is_next_point = self.teacher.current_grid_point_position.x >= self.teacher.current_action.next_point.x and self.teacher.current_grid_point_position.y == self.teacher.current_action.next_point.y
        elif walk_direction == MovementDirection.UP:
            is_next_point = self.teacher.current_grid_point_position.x == self.teacher.current_action.next_point.x and self.teacher.current_grid_point_position.y <= self.teacher.current_action.next_point.y
        elif walk_direction == MovementDirection.DOWN:
            is_next_point = self.teacher.current_grid_point_position.x == self.teacher.current_action.next_point.x and self.teacher.current_grid_point_position.y >= self.teacher.current_action.next_point.y

        if is_next_point: 
            self.teacher.current_grid_point_position = self.teacher.current_action.next_point
            self.teacher.current_action.advance_path()
            if self.teacher.current_action.next_point is None:
                self.teacher.current_action = None
            return

        # Muda os pontos de coordenada para movimentar o professor.
        if walk_direction == MovementDirection.LEFT:
            self.teacher.current_grid_point_position.x -= self.teacher.walk_speed
        elif walk_direction == MovementDirection.RIGHT:
            self.teacher.current_grid_point_position.x += self.teacher.walk_speed
        elif walk_direction == MovementDirection.UP:
            self.teacher.current_grid_point_position.y -= self.teacher.walk_speed
        elif walk_direction == MovementDirection.DOWN:
            self.teacher.current_grid_point_position.y += self.teacher.walk_speed


    def animate_wait(self):
        self.teacher.direction = self.teacher.current_action.direction
        if self.teacher.current_action.wait_time_start == 0:
            self.teacher.current_action.start_timer()
        time_passed = self.teacher.current_action.get_time_passed()
        if time_passed >= self.teacher.sleep_time_threshold and not self.teacher.is_sleeping:
            self.teacher.is_sleeping = True
            self.teacher.current_action.wait_time += self.teacher.time_to_wake_up
        if time_passed >= self.teacher.current_action.wait_time:
            self.wait_time_start = 0
            self.teacher.is_sleeping = False
            self.teacher.current_action = None

    def render_sprite(self, surface: pygame.Surface):
        # corpo
        size_w = 60
        size_h = size_w / 2
        if self.teacher.direction in (MovementDirection.UP, MovementDirection.DOWN):
            pygame.draw.ellipse(surface, 'green', (self.teacher.current_grid_point_position.x - size_w / 2, self.teacher.current_grid_point_position.y - size_h / 2, size_w, size_h), 20)
        if self.teacher.direction in (MovementDirection.LEFT, MovementDirection.RIGHT):
            pygame.draw.ellipse(surface, 'green', (self.teacher.current_grid_point_position.x - size_h / 2, self.teacher.current_grid_point_position.y - size_w / 2, size_h, size_w), 20)

        # cabeça
        pygame.draw.circle(surface, 'black', (self.teacher.current_grid_point_position.x, self.teacher.current_grid_point_position.y), 20)

        # se estiver dormindo
        if self.teacher.is_sleeping:
            pygame.draw.circle(surface, 'blue', (self.teacher.current_grid_point_position.x, self.teacher.current_grid_point_position.y), 5)

        