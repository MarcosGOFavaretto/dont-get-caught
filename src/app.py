from pygame import Surface
from enum import Enum
from .game.render import GameRender

class Screens(Enum):
    MENU = 'MENU'
    GAME_RUNTIME = 'GAME_RUNTIME'
    SETTINGS = 'SETTINGS'
    CREDITS = 'CREDITS'

class App:
    def __init__(self, surface: Surface):
        self.surface = surface
        self.current_render = GameRender(self)

    def render(self):
        self.current_render.render()
        
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
            pass
        elif screen == Screens.GAME_RUNTIME:
            self.current_render = GameRender(self)
        elif screen == Screens.SETTINGS:
            pass
        elif screen == Screens.CREDITS:
            pass

