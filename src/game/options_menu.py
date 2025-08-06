from ..config import WINDOW_HEIGHT, WINDOW_WIDTH
import pygame
from ..components import Button
from .. import fonts
from ..timer import Timer, TIME_SECOND

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .render import GameRender

class OptionsMenu:
    def __init__(self, game: 'GameRender'):
        self.game = game
        self.surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.darken_animation_timer = Timer(wait_time=0.5 * TIME_SECOND)
        self.darken_animation_timer.start()
        self.screen_opacity = 0

    def render(self, on_close_menu = None):
        self.fade_in_animation(start=0, end=220, velocity=10)

        self.surface.fill((0, 0, 0, self.screen_opacity))

        Button(surface=self.surface,
                label='Voltar ao jogo', 
                label_font=fonts.game_final_btn_label,
                background_color=pygame.Color(255, 255, 255),
                rect=pygame.Rect(WINDOW_WIDTH // 2 - 300 // 2, 200, 300, 50), 
                on_click=on_close_menu,
                event_list=self.game.app.event_list)
        
        Button(surface=self.surface,
                label='Sair do jogo', 
                label_font=fonts.game_final_btn_label,
                background_color=pygame.Color(255, 255, 255),
                rect=pygame.Rect(WINDOW_WIDTH // 2 - 300 // 2, 300, 300, 50),
                on_click=self.exit_game,
                event_list=self.game.app.event_list)

        self.game.app.surface.blit(self.surface, (0, 0))      

    def exit_game(self):
        self.game.app.go_to_menu()

    def fade_in_animation(self, start: int, end: int, velocity: int = 1):
        if self.screen_opacity + velocity < end:
            self.screen_opacity += start + velocity