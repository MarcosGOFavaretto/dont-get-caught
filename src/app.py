from tkinter import Menu
from typing import Any
from pygame import Surface
from pygame.event import Event
from pygame_gui import UIManager

from .ui.utils import show_error_toast

from .auth.signup import SignupRender
from .auth.login import LoginRender
from .enums import GameLevels
from .game.render import GameRender
from .menu.render import MenuRender
from .service import user_service, service_utils
import pygame_gui
from .config import THEME_UI_FILE, WINDOW_WIDTH, WINDOW_HEIGHT
class App:
    def __init__(self, surface: Surface):
        self.surface = surface
        self.ui_manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT), theme_path=THEME_UI_FILE)
        self.current_render: Any = None
        self.fase_atual = +1
        self.overlay_render = None
        self.cola_frase_atual = None           
        self.cola_texto_digitado = ""
        self.must_quit = False
        self.time_delta = 0.0
        self.user_profile: dict | None = None
        self.set_initial_render()

    def set_initial_render(self):
        try:
            self.profile = user_service.profile_me()
            self.go_to_menu()
        except service_utils.ServiceError as se:
            if se.error == 'error.auth.token.incorrect':
                self.go_to_login()
                return
            show_error_toast(self.ui_manager, se.get_translated_message())

    def render(self, event_list: list[Event], time_delta: float):
        self.time_delta = time_delta
        self.event_list = event_list
        self.current_render.render()
        if self.overlay_render:
            self.overlay_render.render()
        return self.must_quit
        
    def quit(self):
        self.must_quit = True

    def go_to_menu(self):
        self.current_render = MenuRender(self)

    def start_game(self, selected_level: GameLevels):
        self.current_render = GameRender(self, selected_level=selected_level)

    def go_to_signup(self):
        self.current_render = SignupRender(self)

    def go_to_login(self):
        self.current_render = LoginRender(self)
