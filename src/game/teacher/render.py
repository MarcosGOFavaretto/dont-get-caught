from .movement import MovementDirection, MovementActionType, MovementActionWalk, MovementActionWait
import pygame
import math
from ...config import ASSETS_FOLDER, WINDOW_WIDTH, WINDOW_HEIGHT
from ...timer import Timer
from ...utils import heuristic, senoide, circular, heuristic
from ...fonts import teacher_zzz
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..render import GameRender
    from .teacher import Teacher

class TeacherRender:
    def __init__(self, game: 'GameRender', teacher: 'Teacher'):
        self.game = game
        self.surface = game.app.surface
        self.teacher = teacher
        self.teacher_ends_current_action = False
        self.footstep_interval = 800/self.teacher.walk_speed
        self.footstep_sound_timer = Timer(wait_time=self.footstep_interval)
        self.footstep_volume_fn = lambda x, k: 1 / (1 + math.pow(math.e, k * (x - (5 / k))))
        self.action_timer = Timer()
        self.sleeping_timer = Timer()
        self.action_start_timer = 0
        self.teacher_sprite = pygame.image.load(f'{ASSETS_FOLDER}/images/teacher.png')
        self.teacher_foot_sprite = pygame.image.load(f'{ASSETS_FOLDER}/images/teacher-foot.png')


    def render(self):
        if self.game.game_ends or not self.game.started:
            self.render_sprite()
            return

        if self.teacher.current_action is None or self.teacher_ends_current_action:
            self.next_action()
            if self.teacher.current_action is not None: self.update_sprites_direction(self.teacher.current_action.direction)
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
            self.update_sprites_direction(self.teacher.current_action.direction)
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
            self.sleeping_timer.start()
            self.teacher.is_sleeping = True
            self.teacher.current_action.wait_time += self.teacher.time_to_wake_up
        if time_passed >= self.teacher.current_action.wait_time:
            self.sleeping_timer.stop()
            self.wait_time_start = 0
            self.teacher.is_sleeping = False
            self.teacher_ends_current_action = True

    def render_sprite(self):
        if not self.teacher.is_sleeping and self.game.started:
            self.render_vision()
        self.surface.blit(self.teacher_sprite, (self.teacher.position.x - 32, self.teacher.position.y - 32))
        if self.teacher.is_sleeping:
            self.render_sleeping_animation()

    def update_sprites_direction(self, direction: MovementDirection):
        directions_map = self.teacher.direction.get_directions_rotation_map()
        rotation_degrees = directions_map[direction]
        self.teacher_sprite = pygame.transform.rotate(self.teacher_sprite, rotation_degrees)
        self.teacher_foot_sprite = pygame.transform.rotate(self.teacher_foot_sprite, rotation_degrees)

    def render_sleeping_animation(self):
        radius = 24
        velocity = 0.002
        sleeping_time = self.sleeping_timer.get_time_passed()
        z1 = circular(self.teacher.position.x, self.teacher.position.y, radius, velocity, 0, sleeping_time)
        z2 = circular(self.teacher.position.x, self.teacher.position.y, radius, velocity, math.pi, sleeping_time)
        text_surface = teacher_zzz.render('ZzZ', True, 'blue')
        z1_text = text_surface.get_rect(center=z1)
        z2_text = text_surface.get_rect(center=z2)
        self.surface.blit(text_surface, z1_text)
        self.surface.blit(text_surface, z2_text)


    def render_foots_movement(self):
        movement_amplitude = senoide(self.teacher.step_amplitude, 1/(self.footstep_interval * 2), -math.pi/2, 0, self.action_timer.get_time_passed(), square_shapping=0.08)
        left_foot_offset = movement_amplitude
        right_foot_offset = -left_foot_offset
        if self.teacher.direction == MovementDirection.DOWN:
            self.surface.blit(self.teacher_foot_sprite, (self.teacher.position.x - self.teacher.foot_dist - 32 , self.teacher.position.y + left_foot_offset - 32)) # left foot
            self.surface.blit(self.teacher_foot_sprite, (self.teacher.position.x + self.teacher.foot_dist - 32, self.teacher.position.y + right_foot_offset - 32)) # right foot
        if self.teacher.direction == MovementDirection.UP:
            self.surface.blit(self.teacher_foot_sprite, (self.teacher.position.x - self.teacher.foot_dist - 32 , self.teacher.position.y - left_foot_offset - 32)) # left foot
            self.surface.blit(self.teacher_foot_sprite, (self.teacher.position.x + self.teacher.foot_dist - 32, self.teacher.position.y - right_foot_offset - 32)) # right foot
        if self.teacher.direction == MovementDirection.LEFT:
            self.surface.blit(self.teacher_foot_sprite, (self.teacher.position.x - left_foot_offset - 32 , self.teacher.position.y - self.teacher.foot_dist - 32)) # left foot
            self.surface.blit(self.teacher_foot_sprite, (self.teacher.position.x - right_foot_offset - 32, self.teacher.position.y + self.teacher.foot_dist - 32)) # right foot
        if self.teacher.direction == MovementDirection.RIGHT:
            self.surface.blit(self.teacher_foot_sprite, (self.teacher.position.x + left_foot_offset - 32 , self.teacher.position.y - self.teacher.foot_dist - 32)) # left foot
            self.surface.blit(self.teacher_foot_sprite, (self.teacher.position.x + right_foot_offset - 32, self.teacher.position.y + self.teacher.foot_dist - 32)) # right foot
        
        
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
        sound_volume = self.footstep_volume_fn(teacher_student_dist // 100, 2)
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