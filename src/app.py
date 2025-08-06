from pygame import Surface
from pygame.event import Event
from pygame_gui import UIManager

from .auth.render import AuthRender
from .enums import GameLevels
from .game.render import GameRender
from .menu.render import MenuRender

class App:
    def __init__(self, surface: Surface, ui_manager: UIManager):
        self.surface = surface
        self.ui_manager = ui_manager
        self.current_render = AuthRender(self)
        self.fase_atual = +1
        self.overlay_render = None
        self.cola_frase_atual = None           
        self.cola_texto_digitado = ""
        self.must_quit = False
        self.time_delta = 0.0

    def render(self, event_list: list[Event], time_delta: float):
        self.time_delta = time_delta
        self.event_list = event_list
        self.current_render.render()
        if self.overlay_render:
            self.overlay_render.render()
        return self.must_quit
        
    def quit(self):
        self.must_quit = True

    def open_menu(self):
        self.current_render = MenuRender(self)

    def start_game(self, selected_level: GameLevels):
        self.current_render = GameRender(self, selected_level=selected_level)

