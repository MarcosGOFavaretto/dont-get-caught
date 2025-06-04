from pygame import Surface
from .enums import GameLevels
from .game.render import GameRender
from .menu.render import MenuRender
from .cola.render import ColaRender
from pygame.event import Event  
from .cola.render import ColaRender

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

    def open_cola(self):
        dificuldade = self.get_dificuldade()
        self.current_render = ColaRender(self, dificuldade)

    def get_dificuldade(self):
        if hasattr(self, "fase_atual"):
            return min(self.fase_atual, 3)
        return 1
    
    def start_cola_overlay(self):
        dificuldade = self.get_dificuldade()
        self.overlay_render = ColaRender(
            self,
            dificuldade,
            self.cola_frase_atual,
            self.cola_texto_digitado
        )

    def close_cola_overlay(self, frase_atual, texto_digitado):
        print("Texto colado:", texto_digitado)
        self.cola_frase_atual = frase_atual
        self.cola_texto_digitado = texto_digitado
        self.overlay_render = None


    def handle_event(self, event):
        if self.overlay_render:
            self.overlay_render.handle_event(event)
        else:
            if hasattr(self.current_render, 'handle_event'):
                self.current_render.handle_event(event)

