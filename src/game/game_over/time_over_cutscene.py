import pygame

from ...utils import senoide
from ...timer import Timer, TIME_SECOND
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..render import GameRender
from ...config import ASSETS_FOLDER, EXAM_TIME
from ...timer import time_to_string
from ...fonts import clock as clock_font

class TimeOverCutscene():
    def __init__(self, game: 'GameRender'):
        self.game = game
        self.cutscene_time = Timer(wait_time=3 * TIME_SECOND)
        self.render_started = False
        self.clock_alarm_sound = pygame.mixer.Sound(f'{ASSETS_FOLDER}/sounds/clock-alarm.mp3')

        rotation = 2

        self.clock_left_rotation = pygame.transform.rotate(self.game.clock_sprite, -rotation)
        self.clock_right_rotation = pygame.transform.rotate(self.game.clock_sprite, rotation)

        self.clock_surface = clock_font.render(time_to_string(0), True, 'red')
        self.clock_surface_left_rotation = pygame.transform.rotate(self.clock_surface, -rotation)
        self.clock_surface_right_rotation = pygame.transform.rotate(self.clock_surface, -rotation)
        self.rotated_rect = self.clock_surface_left_rotation.get_rect(center=self.clock_surface.get_rect().center)

        self.clock_sprites = [self.game.clock_sprite, self.clock_left_rotation, self.game.clock_sprite, self.clock_right_rotation]
        self.clock_time_surfaces = [self.clock_surface, self.clock_surface_left_rotation, self.clock_surface, self.clock_surface_right_rotation]
        self.current_sprite = 0

    def setup(self):
        self.cutscene_time.start()
        self.clock_alarm_sound.play()
        self.render_started = True

    def render(self, on_ends):
        if not self.render_started:
            self.setup()
            return
        
        if self.cutscene_time.time_is_up():
            self.clock_alarm_sound.stop()
            on_ends()
            return
        
        self.game.app.surface.blit(self.clock_sprites[self.current_sprite], (-6, -36))
        self.game.app.surface.blit(self.clock_time_surfaces[self.current_sprite], (24, 18))

        self.current_sprite += 1
        if self.current_sprite >= len(self.clock_sprites):
            self.current_sprite = 0



        
