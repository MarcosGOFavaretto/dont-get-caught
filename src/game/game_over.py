from ..config import WINDOW_HEIGHT, WINDOW_WIDTH
import pygame
from ..components import Button, Text
from .. import fonts
from ..timer import Timer, TIME_SECOND

class GameOver:
    def __init__(self, app):
        self.app = app
        self.surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.darken_animation_timer = Timer(wait_time=0.5 * TIME_SECOND)
        self.darken_animation_timer.start()
        self.screen_opacity = 0

    def render(self):
        self.fade_in_animation(step=5)

        self.surface.fill((0, 0, 0, self.screen_opacity))

        Text(surface=self.surface,
                content='GAME OVER',
                color=(255, 255, 255, self.screen_opacity),
                position=(WINDOW_WIDTH // 2, 200),
                font=fonts.game_over_title,
                outline_color=(0, 0, 0),
                outline_size=2)

        Button(surface=self.surface,
                label='JOGAR NOVAMENTE', 
                label_font=fonts.game_over_btn_label,
                background_color=(255, 255, 255),
                rect=pygame.Rect(WINDOW_WIDTH // 2 - 300 // 2, 260, 300, 50))

        self.app.surface.blit(self.surface, (0, 0))      

    def fade_in_animation(self, step: int):
        if not self.darken_animation_timer.time_is_up() and self.screen_opacity + step < 255:
            self.screen_opacity += step