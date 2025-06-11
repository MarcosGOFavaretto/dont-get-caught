from pygame import Surface
from pygame.event import Event
from .enums import GameLevels
from .game.render import GameRender
from .menu.render import MenuRender

class App:
    def __init__(self, surface: Surface):
        self.surface = surface
        self.current_render = MenuRender(self)
        self.fase_atual = +1
        self.overlay_render = None
        self.cola_frase_atual = None           
        self.cola_texto_digitado = ""

    def render(self, event_list: list[Event]):
        self.event_list = event_list
        self.current_render.render()
        if self.overlay_render:
            self.overlay_render.render()
        
    def open_menu(self):
        self.current_render = MenuRender(self)

    def start_game(self, selected_level: GameLevels):
        self.current_render = GameRender(self, selected_level=selected_level)

    # def close_cola_overlay(self, frase_atual, texto_digitado):
    #     self.cola_frase_atual = frase_atual
    #     self.cola_texto_digitado = texto_digitado
    #     self.overlay_render = None

