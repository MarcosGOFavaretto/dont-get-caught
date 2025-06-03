import pygame
from ..fonts import menu as menu_font
from ..config import WINDOW_HEIGHT, WINDOW_WIDTH, ASSETS_FOLDER
from ..enums import GameLevels
from ..components import Button

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..app import App

class MenuRender:
    def __init__(self, app: 'App'):
        self.app = app
        self.background = pygame.image.load(f"{ASSETS_FOLDER}/menu-background.png")
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.buttons_width = 260
        self.background_sound = pygame.mixer.Sound(f'{ASSETS_FOLDER}/background-sound-menu.mp3')
        self.background_sound.play(loops=-1, fade_ms=2000)
        self.background_sound.set_volume(0.2)

        self.button_click_fx = pygame.mixer.Sound(f'{ASSETS_FOLDER}/menu-click-btn.mp3')
        self.button_back_fx = pygame.mixer.Sound(f'{ASSETS_FOLDER}/menu-back-btn.mp3')

        self.button_click_fx.set_volume(0.5)
        self.button_back_fx.set_volume(0.5)

        self.menu_active = True
        self.difficulty_menu_active = False
        self.how_to_play_active = True

    def render(self):
        self.app.surface.blit(self.background, (0, 0))
        if self.menu_active:
            self.render_menu_options()
        elif self.difficulty_menu_active:
            self.render_levels_options()

    def render_menu_options(self):
        Button(surface=self.app.surface,
            label='INICIAR', 
            label_font=menu_font,
            background_color=pygame.Color(255, 255, 255),
            rect=pygame.Rect(WINDOW_WIDTH // 2 - self.buttons_width // 2, 260, self.buttons_width, 50),
            on_click=self.open_levels,
            event_list=self.app.event_list)
        
        Button(surface=self.app.surface,
            label='OPÇÕES', 
            label_font=menu_font,
            background_color=pygame.Color(255, 255, 255),
            rect=pygame.Rect(WINDOW_WIDTH // 2 - self.buttons_width // 2, 340, self.buttons_width, 50))
        
        Button(surface=self.app.surface,
            label='SAIR', 
            label_font=menu_font,
            background_color=pygame.Color(255, 255, 255),
            rect=pygame.Rect(WINDOW_WIDTH // 2 - self.buttons_width // 2, 420, self.buttons_width, 50),
            on_click=lambda: pygame.quit(),
            event_list=self.app.event_list)


    def render_levels_options(self):
        Button(surface=self.app.surface,
            label='FÁCIL',
            label_font=menu_font,
            background_color=pygame.Color(255, 255, 255),
            rect=pygame.Rect(WINDOW_WIDTH // 2 - self.buttons_width // 2, 260, self.buttons_width, 50),
            on_click=lambda: self.set_level(GameLevels.EASY),
            event_list=self.app.event_list)

        Button(surface=self.app.surface,
            label='MÉDIO',
            label_font=menu_font,
            background_color=pygame.Color(255, 255, 255),
            rect=pygame.Rect(WINDOW_WIDTH // 2 - self.buttons_width // 2, 340, self.buttons_width, 50),
            on_click=lambda: self.set_level(GameLevels.MEDIUM),
            event_list=self.app.event_list)

        Button(surface=self.app.surface,
            label='DIFÍCIL',
            label_font=menu_font,
            background_color=pygame.Color(255, 255, 255),
            rect=pygame.Rect(WINDOW_WIDTH // 2 - self.buttons_width // 2, 420, self.buttons_width, 50),
            on_click=lambda: self.set_level(GameLevels.HARD),
            event_list=self.app.event_list)
        
        Button(surface=self.app.surface,
            label='VOLTAR', 
            label_font=menu_font,
            rect=pygame.Rect(WINDOW_WIDTH // 2 - self.buttons_width // 2, 500, self.buttons_width, 50),
            on_click=self.onclick_back,
            event_list=self.app.event_list)

    def open_levels(self):
        self.button_click_fx.play()
        self.menu_active = False
        self.difficulty_menu_active = True

    def onclick_back(self):
        self.menu_active = True
        self.difficulty_menu_active = False
        self.button_back_fx.play()

    def set_level(self, level: GameLevels):
        self.button_click_fx.play()
        self.background_sound.stop()
        self.app.start_game(level)