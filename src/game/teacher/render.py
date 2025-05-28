from .movement import MovementDirection, MovementActionType, MovementActionWalk, MovementActionWait
import pygame
import math
from ...config import WINDOW_WIDTH, WINDOW_HEIGHT
from ...timer import Timer
from ...utils import heuristic, map_value, senoide
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..render import GameRender
    from .teacher import Teacher

class TeacherRender:
    def __init__(self, game: 'GameRender', teacher: 'Teacher', surface: pygame.Surface):
        self.surface = surface
        self.teacher = teacher
        self.teacher_ends_current_action = False
        self.footstep_interval = 800/self.teacher.walk_speed
        self.footstep_sound_timer = Timer(wait_time=self.footstep_interval)
        self.action_timer = Timer()
        self.action_start_timer = 0
        self.game = game
        # self.footstep_movement_fn = senoide(12, 1/(self.footstep_interval * 2), math.pi/2)

    def render(self):
        if self.game.game_ends:
            self.render_sprite()
            return

        if self.teacher.current_action is None or self.teacher_ends_current_action:
            self.next_action()
            self.action_timer.restart()

        if self.teacher.current_action is None:
            raise ValueError("Teacher has no current action to render.")

        if self.teacher.current_action.action_type == MovementActionType.WALK:
            self.teacher_ends_current_action = False
            self.teacher.is_walking = True
            self.animate_walk()
        elif self.teacher.current_action.action_type == MovementActionType.WAIT:
            self.footstep_sound_timer.stop()
            self.teacher_ends_current_action = False
            self.teacher.is_waiting = True
            self.animate_wait()

        self.render_sprite()

    def next_action(self):
        self.teacher.is_waiting = False
        self.teacher.is_walking = False
        self.teacher.get_next_action()
    
    def animate_walk(self):
        self.render_foots_movement()
        self.play_footstep_sound()

        if self.footstep_sound_timer.time_is_up():
            self.footstep_sound_timer.restart()

        if self.teacher.current_action is None:
            raise ValueError("Teacher has no current action to render.")

        if not isinstance(self.teacher.current_action, MovementActionWalk):
            raise ValueError("Current action is not a walking action.")

        walk_direction = self.teacher.current_action.direction
        self.teacher.direction = walk_direction
        self.teacher.vision_direction = walk_direction

        if self.teacher.current_action.next_point is None:
            raise ValueError("Next point is None, cannot animate walk.")

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
        if not isinstance(self.teacher.current_action, MovementActionWait):
            raise ValueError("Current action is not a wait action.")
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
        size_h = size_w // 2
        if self.teacher.direction in (MovementDirection.UP, MovementDirection.DOWN):
            pygame.draw.ellipse(self.surface, 'green', (self.teacher.position.x - size_w // 2, self.teacher.position.y - size_h // 2, size_w, size_h), 20)
        if self.teacher.direction in (MovementDirection.LEFT, MovementDirection.RIGHT):
            pygame.draw.ellipse(self.surface, 'green', (self.teacher.position.x - size_h // 2, self.teacher.position.y - size_w // 2, size_h, size_w), 20)
        # cabeça
        pygame.draw.circle(self.surface, 'black', (self.teacher.position.x, self.teacher.position.y), 20)
        # se estiver dormindo
        if self.teacher.is_sleeping:
            pygame.draw.circle(self.surface, 'blue', (self.teacher.position.x, self.teacher.position.y), 5)

    def render_foots_movement(self):
        movement_amplitude = senoide(self.teacher.step_amplitude, 1/(self.footstep_interval * 2), -90, 0, 0.2, self.action_timer.get_time_passed())
        left_foot_offset = movement_amplitude
        right_foot_offset = -left_foot_offset

        if self.teacher.direction == MovementDirection.DOWN:
            pygame.draw.circle(self.surface, 'brown', (self.teacher.position.x - self.teacher.foot_dist, self.teacher.position.y+left_foot_offset), self.teacher.foot_size) # left foot
            pygame.draw.circle(self.surface, 'brown', (self.teacher.position.x + self.teacher.foot_dist, self.teacher.position.y+right_foot_offset), self.teacher.foot_size) # right foot

        if self.teacher.direction == MovementDirection.UP:
            pygame.draw.circle(self.surface, 'brown', (self.teacher.position.x - self.teacher.foot_dist, self.teacher.position.y-left_foot_offset), self.teacher.foot_size) # left foot
            pygame.draw.circle(self.surface, 'brown', (self.teacher.position.x + self.teacher.foot_dist, self.teacher.position.y-right_foot_offset), self.teacher.foot_size) # right foot
            
        if self.teacher.direction == MovementDirection.LEFT:
            pygame.draw.circle(self.surface, 'brown', (self.teacher.position.x - left_foot_offset, self.teacher.position.y-self.teacher.foot_dist), self.teacher.foot_size) # left foot
            pygame.draw.circle(self.surface, 'brown', (self.teacher.position.x - right_foot_offset, self.teacher.position.y+self.teacher.foot_dist), self.teacher.foot_size) # right foot
        
        if self.teacher.direction == MovementDirection.RIGHT:
            pygame.draw.circle(self.surface, 'brown', (self.teacher.position.x + left_foot_offset, self.teacher.position.y-self.teacher.foot_dist), self.teacher.foot_size) # left foot
            pygame.draw.circle(self.surface, 'brown', (self.teacher.position.x + right_foot_offset, self.teacher.position.y+self.teacher.foot_dist), self.teacher.foot_size) # right foot
        
        
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

        if sound_volume < 0:
            sound_volume = 0
        elif sound_volume > 1:
            sound_volume = 1

        self.teacher.footstep_sound.set_volume(sound_volume)

        if not self.footstep_sound_timer.is_counting:
            self.footstep_sound_timer.start()
            self.teacher.footstep_sound.play()
        if self.footstep_sound_timer.time_is_up():
            self.teacher.footstep_sound.play()