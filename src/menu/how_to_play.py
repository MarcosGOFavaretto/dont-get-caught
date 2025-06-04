import pygame
from ..fonts import menu_sm, menu_lg
from ..config import WINDOW_WIDTH, ASSETS_FOLDER, WINDOW_HEIGHT
from ..components import Button, Text

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .render import MenuRender

from ..enums import MenuPage

class MenuHowToPlay:
    def __init__(self, menu: 'MenuRender') -> None:
        self.menu = menu
        self.background = pygame.image.load(f"{ASSETS_FOLDER}/menu-background-nologo.jpg")
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.margin_x = 20
        self.margin_top = 20
        self.surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)

        self.controls = [
            dict(command='Ctrl + C', description='Abrir cola'),
            dict(command='Esc', description='Sair da cola'),
        ]

    def render(self):
        self.menu.app.surface.blit(self.background, (0, 0))
        controls_area = pygame.draw.rect(self.surface, pygame.Color(255, 255, 255, 200), pygame.Rect(self.margin_top, self.margin_x, WINDOW_WIDTH - 2 * self.margin_x, 460))
        self.render_controls(controls_area)
        self.menu.app.surface.blit(self.surface, (0, 0))
        Button(surface=self.menu.app.surface,
            label='VOLTAR', 
            label_font=menu_lg,
            rect=pygame.Rect(WINDOW_WIDTH // 2 - self.menu.buttons_width // 2, 500, self.menu.buttons_width, 50),
            on_click=self.onclick_back,
            event_list=self.menu.app.event_list)
        
    def render_controls(self, controls_area: pygame.Rect):
        line_spacing = 50
        for i, control in enumerate(self.controls):
            y = i * line_spacing + controls_area.top + 40
            Text(surface=self.surface,
                content=control['command'],
                color=pygame.Color(0, 0, 0),
                outline_color=pygame.Color(255, 255, 255),
                outline_size=2,
                position=(controls_area.left + 40, y),
                font=menu_lg)
            
            Text(surface=self.surface,
                content=control['description'],
                color=pygame.Color(0, 0, 0),
                outline_color=pygame.Color(255, 255, 255),
                outline_size=2,
                position=(controls_area.left + controls_area.width // 2, y + 10),
                font=menu_sm)

    def onclick_back(self):
        self.menu.active_page = MenuPage.MAIN
        self.menu.button_back_fx.play()