import pygame
from ..fonts import menu_lg
from ..config import WINDOW_WIDTH
from ..enums import GameLevels
from ..components import Button

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .render import MenuRender

from ..enums import MenuPage

class MenuLevels:
    def __init__(self, menu: 'MenuRender') -> None:
        self.menu = menu
        self.buttons_initial_y = 300
        self.buttons_spacing_y = 80

    def render(self):
        self.menu.app.surface.blit(self.menu.background, (0, 0))
        Button(surface=self.menu.app.surface,
            label='FACIL',
            label_font=menu_lg,
            background_color=pygame.Color(255, 255, 255),
            rect=pygame.Rect(WINDOW_WIDTH // 2 - self.menu.buttons_width // 2, self.buttons_initial_y, self.menu.buttons_width, 50),
            on_click=lambda: self.set_level(GameLevels.EASY),
            event_list=self.menu.app.event_list)

        Button(surface=self.menu.app.surface,
            label='MEDIO',
            label_font=menu_lg,
            background_color=pygame.Color(255, 255, 255),
            rect=pygame.Rect(WINDOW_WIDTH // 2 - self.menu.buttons_width // 2, self.buttons_initial_y + self.buttons_spacing_y, self.menu.buttons_width, 50),
            on_click=lambda: self.set_level(GameLevels.MEDIUM),
            event_list=self.menu.app.event_list)

        Button(surface=self.menu.app.surface,
            label='DIFICIL',
            label_font=menu_lg,
            background_color=pygame.Color(255, 255, 255),
            rect=pygame.Rect(WINDOW_WIDTH // 2 - self.menu.buttons_width // 2, self.buttons_initial_y + self.buttons_spacing_y * 2, self.menu.buttons_width, 50),
            on_click=lambda: self.set_level(GameLevels.HARD),
            event_list=self.menu.app.event_list)
        
        Button(surface=self.menu.app.surface,
            label='VOLTAR', 
            label_font=menu_lg,
            rect=pygame.Rect(WINDOW_WIDTH // 2 - self.menu.buttons_width // 2, self.buttons_initial_y + self.buttons_spacing_y * 3, self.menu.buttons_width, 50),
            on_click=self.onclick_back,
            event_list=self.menu.app.event_list)
        
    def onclick_back(self):
        self.menu.active_page = MenuPage.MAIN
        self.menu.button_back_fx.play()

    def set_level(self, level: GameLevels):
        self.menu.button_click_fx.play()
        self.menu.background_sound.stop()
        self.menu.app.start_game(level)