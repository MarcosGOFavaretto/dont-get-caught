from pygame import Surface
from .screens import Screens
from .game.render import GameRender
from .menu.render import MenuRender
from .cola.render import ColaRender  

class App:
    def __init__(self, surface: Surface):
        self.surface = surface
        self.current_render = MenuRender(self)
        self.fase_atual = +1
        self.overlay_render = None
        self.cola_frase_atual = None           
        self.cola_texto_digitado = ""

    def render(self):
        self.current_render.render()
        if self.overlay_render:
            self.overlay_render.render()
        
    def open_menu(self):
        self.set_render(Screens.MENU)

    def start_game(self):
        self.set_render(Screens.GAME_RUNTIME)

    def open_settings(self):
        self.set_render(Screens.SETTINGS)

    def open_credits_page(self):
        self.set_render(Screens.CREDITS)

    def set_render(self, screen: Screens):
        if screen == Screens.MENU:
            self.current_render = MenuRender(self)
        elif screen == Screens.GAME_RUNTIME:
            self.current_render = GameRender(self)
        elif screen == Screens.COLA:
            from.cola.render import ColaRender
            dificuldade = self.get_dificuldade()
            self.current_render = ColaRender(self, dificuldade)
        elif screen == Screens.SETTINGS:
            pass
        elif screen == Screens.CREDITS:
            pass

    def get_dificuldade(self):
        if hasattr(self, "fase_atual"):
            return min(self.fase_atual, 3)
        return 1
    
    def start_cola_overlay(self):
        from .cola.render import ColaRender
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
            self.current_render.handle_event(event)

