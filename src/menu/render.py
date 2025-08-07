import pygame

from ..ui.utils import show_error_toast

from ..fonts import menu_lg
from ..config import WINDOW_HEIGHT, WINDOW_WIDTH, ASSETS_FOLDER
from ..components import Button

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..app import App

from .levels import MenuLevels
from .how_to_play import MenuHowToPlay
from ..enums import MenuPage
from ..service import user_service, service_utils
import pygame_gui

class MenuRender:
    def __init__(self, app: 'App'):
        self.app = app
        self.background = pygame.image.load(f"{ASSETS_FOLDER}/images/menu-background.png")
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.buttons_width = 260

        self.background_sound = pygame.mixer.Sound(f'{ASSETS_FOLDER}/sounds/background-sound-menu.mp3')
        self.background_sound.play(loops=-1, fade_ms=2000)
        self.background_sound.set_volume(0.1)
        self.button_click_fx = pygame.mixer.Sound(f'{ASSETS_FOLDER}/sounds/menu-click-btn.mp3')
        self.button_back_fx = pygame.mixer.Sound(f'{ASSETS_FOLDER}/sounds/menu-back-btn.mp3')
        self.button_click_fx.set_volume(0.5)
        self.button_back_fx.set_volume(0.5)

        self.menu_active = True
        self.difficulty_menu_active = False
        self.how_to_play_active = True

        self.active_page: MenuPage = MenuPage.MAIN
        self.menu_levels = MenuLevels(self)
        self.menu_how_to_play = MenuHowToPlay(self)

        self.buttons_initial_y = 300
        self.buttons_spacing_y = 100

    def render(self):
        match self.active_page:
            case MenuPage.MAIN:
                self.render_menu_options()
            case MenuPage.GAME_LEVELS:
                self.menu_levels.render()
            case MenuPage.HOW_TO_PLAY:
                self.menu_how_to_play.render()

    def render_menu_options(self):
        self.app.surface.blit(self.background, (0, 0))
        Button(surface=self.app.surface,
            label='JOGAR', 
            label_font=menu_lg,
            background_color=pygame.Color(255, 255, 255),
            rect=pygame.Rect(WINDOW_WIDTH // 2 - self.buttons_width // 2, self.buttons_initial_y, self.buttons_width, 50),
            on_click=lambda: self.open_page(MenuPage.GAME_LEVELS),
            event_list=self.app.event_list)
        
        Button(surface=self.app.surface,
            label='COMO JOGAR', 
            label_font=menu_lg,
            background_color=pygame.Color(255, 255, 255),
            rect=pygame.Rect(WINDOW_WIDTH // 2 - (self.buttons_width + 100) // 2, self.buttons_initial_y + self.buttons_spacing_y, self.buttons_width + 100, 50),
            on_click=lambda: self.open_page(MenuPage.HOW_TO_PLAY),
            event_list=self.app.event_list)
        
        Button(surface=self.app.surface,
            label='SAIR', 
            label_font=menu_lg,
            background_color=pygame.Color(255, 255, 255),
            rect=pygame.Rect(WINDOW_WIDTH // 2 - self.buttons_width // 2, self.buttons_initial_y + self.buttons_spacing_y * 2, self.buttons_width, 50),
            on_click=self.app.quit,
            event_list=self.app.event_list)

    def open_page(self, menu_page: MenuPage):
        self.button_click_fx.play()
        self.active_page = menu_page