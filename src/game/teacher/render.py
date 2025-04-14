from .movement import MovementDirection, MovementActionType
import pygame
import math
from ...config import WINDOW_WIDTH, WINDOW_HEIGHT

class TeacherRender:
    def __init__(self, teacher, surface: pygame.Surface):
        self.surface = surface
        self.teacher = teacher

    def render(self):
        if self.teacher.current_action is None:
            self.next_action()

        if self.teacher.current_action.action_type == MovementActionType.WALK:
            self.teacher.is_walking = True
            self.animate_walk()
        elif self.teacher.current_action.action_type == MovementActionType.WAIT:
            self.teacher.is_waiting = True
            self.animate_wait()

        self.render_sprite()

    def next_action(self):
        self.teacher.is_waiting = False
        self.teacher.is_walking = False
        self.teacher.current_action = self.teacher.get_next_action()
    
    def animate_walk(self):
        walk_direction = self.teacher.current_action.direction
        self.teacher.direction = walk_direction
        self.teacher.vision_direction = walk_direction

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
        self.teacher.vision_direction = self.teacher.current_action.direction
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


    def render_sprite(self):
        if not self.teacher.is_sleeping:
            self.render_vision()

        vision_points = self.teacher.get_vision_points()
        for point in vision_points:
            pygame.draw.circle(self.surface, 'yellow', (point.x, point.y), 5)

        # corpo
        size_w = 60
        size_h = size_w / 2
        if self.teacher.direction in (MovementDirection.UP, MovementDirection.DOWN):
            pygame.draw.ellipse(self.surface, 'green', (self.teacher.current_grid_point_position.x - size_w / 2, self.teacher.current_grid_point_position.y - size_h / 2, size_w, size_h), 20)
        if self.teacher.direction in (MovementDirection.LEFT, MovementDirection.RIGHT):
            pygame.draw.ellipse(self.surface, 'green', (self.teacher.current_grid_point_position.x - size_h / 2, self.teacher.current_grid_point_position.y - size_w / 2, size_h, size_w), 20)

        # cabeça
        pygame.draw.circle(self.surface, 'black', (self.teacher.current_grid_point_position.x, self.teacher.current_grid_point_position.y), 20)

        # se estiver dormindo
        if self.teacher.is_sleeping:
            pygame.draw.circle(self.surface, 'blue', (self.teacher.current_grid_point_position.x, self.teacher.current_grid_point_position.y), 5)
        
    def render_vision(self):
        vision_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        vision_angle_range = self.teacher.get_vision_angle_range()
        self.draw_filled_semi_circle(vision_surface, (0, 0, 255, 40), (self.teacher.current_grid_point_position.x, self.teacher.current_grid_point_position.y), self.teacher.vision_radius, vision_angle_range[0], vision_angle_range[1])
        self.surface.blit(vision_surface, (0, 0))
    
    def draw_filled_semi_circle(self, surface, color, center, radius, start_angle, end_angle, point_count=50):
        points = [center]
        for i in range(point_count + 1):
            angle = start_angle + (end_angle - start_angle) * i / point_count
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            points.append((x, y))
        pygame.draw.polygon(surface, color, points)
