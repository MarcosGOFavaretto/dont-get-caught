from .movement import MovementDirection, MovementActionType
import pygame
import math
from ...config import WINDOW_WIDTH, WINDOW_HEIGHT
from ...timer import Timer
from ...utils import heuristic, map_value
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..render import GameRender

class TeacherRender:
    def __init__(self, game: 'GameRender', teacher, surface: pygame.Surface):
        self.surface = surface
        self.teacher = teacher
        self.teacher_ends_current_action = False
        self.footstep_timer = Timer(wait_time=800/self.teacher.walk_speed)
        self.game = game

    def render(self):
        if self.game.game_ends:
            self.render_sprite()
            return

        if self.teacher.current_action is None or self.teacher_ends_current_action:
            self.next_action()

        if self.teacher.current_action.action_type == MovementActionType.WALK:
            self.teacher_ends_current_action = False
            self.teacher.is_walking = True
            self.play_footstep_sound()
            self.animate_walk()
        elif self.teacher.current_action.action_type == MovementActionType.WAIT:
            self.teacher_ends_current_action = False
            self.teacher.is_waiting = True
            self.animate_wait()

        self.render_sprite()

    def next_action(self):
        self.teacher.is_waiting = False
        self.teacher.is_walking = False
        self.teacher.get_next_action()
    
    def animate_walk(self):
        walk_direction = self.teacher.current_action.direction
        self.teacher.direction = walk_direction
        self.teacher.vision_direction = walk_direction

        # Verifica se o professor terminou o passo
        is_next_point = False
        if walk_direction == MovementDirection.LEFT:
            is_next_point = self.teacher.position.x <= self.teacher.current_action.next_point.x and self.teacher.position.y == self.teacher.current_action.next_point.y
        elif walk_direction == MovementDirection.RIGHT:
            is_next_point = self.teacher.position.x >= self.teacher.current_action.next_point.x and self.teacher.position.y == self.teacher.current_action.next_point.y
        elif walk_direction == MovementDirection.UP:
            is_next_point = self.teacher.position.x == self.teacher.current_action.next_point.x and self.teacher.position.y <= self.teacher.current_action.next_point.y
        elif walk_direction == MovementDirection.DOWN:
            is_next_point = self.teacher.position.x == self.teacher.current_action.next_point.x and self.teacher.position.y >= self.teacher.current_action.next_point.y

        if is_next_point: 
            self.teacher.position = self.teacher.current_action.next_point
            self.teacher.current_action.advance_path()
            if self.teacher.current_action.next_point is None:
                # self.teacher.current_action = None
                self.teacher_ends_current_action = True
            return

        # Muda os pontos de coordenada para movimentar o professor.
        if walk_direction == MovementDirection.LEFT:
            self.teacher.position.x -= self.teacher.walk_speed
        elif walk_direction == MovementDirection.RIGHT:
            self.teacher.position.x += self.teacher.walk_speed
        elif walk_direction == MovementDirection.UP:
            self.teacher.position.y -= self.teacher.walk_speed
        elif walk_direction == MovementDirection.DOWN:
            self.teacher.position.y += self.teacher.walk_speed

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
            self.teacher_ends_current_action = True

    def render_sprite(self):
        if not self.teacher.is_sleeping:
            self.render_vision()

        # corpo
        size_w = 60
        size_h = size_w / 2
        if self.teacher.direction in (MovementDirection.UP, MovementDirection.DOWN):
            pygame.draw.ellipse(self.surface, 'green', (self.teacher.position.x - size_w / 2, self.teacher.position.y - size_h / 2, size_w, size_h), 20)
        if self.teacher.direction in (MovementDirection.LEFT, MovementDirection.RIGHT):
            pygame.draw.ellipse(self.surface, 'green', (self.teacher.position.x - size_h / 2, self.teacher.position.y - size_w / 2, size_h, size_w), 20)

        # cabeça
        pygame.draw.circle(self.surface, 'black', (self.teacher.position.x, self.teacher.position.y), 20)

        # se estiver dormindo
        if self.teacher.is_sleeping:
            pygame.draw.circle(self.surface, 'blue', (self.teacher.position.x, self.teacher.position.y), 5)
        
    def render_vision(self):
        vision_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        vision_angle_range = self.teacher.get_vision_angle_range()
        self.draw_filled_semi_circle(vision_surface, (0, 0, 255, 40), (self.teacher.position.x, self.teacher.position.y), self.teacher.vision_radius, vision_angle_range[0], vision_angle_range[1])
        self.surface.blit(vision_surface, (0, 0))
    
    def draw_filled_semi_circle(self, surface, color, center, radius, start_angle, end_angle, point_count=50):
        points = [center]
        for i in range(point_count + 1):
            angle = start_angle + (end_angle - start_angle) * i / point_count
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            points.append((x, y))
        pygame.draw.polygon(surface, color, points)

    def play_footstep_sound(self):
        teacher_student_dist = heuristic(self.teacher.position.to_coordenate(), self.game.student.position.to_coordenate())
        sound_volume = map_value(teacher_student_dist, 0, self.game.student.hearing_teacher_steps_range, 1, 0)
        listen_curve = 2
        sound_volume = math.pow(sound_volume, listen_curve)

        if sound_volume < 0:
            sound_volume = 0
        elif sound_volume > 1:
            sound_volume = 1

        self.teacher.footstep_sound.set_volume(sound_volume)

        if not self.footstep_timer.is_counting:
            self.footstep_timer.start()
            self.teacher.footstep_sound.play()
        if self.footstep_timer.time_is_up():
            self.teacher.footstep_sound.play()
            self.footstep_timer.restart()