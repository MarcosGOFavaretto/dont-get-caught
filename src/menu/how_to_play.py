import pygame
from ..fonts import menu_sm, menu_how_to_play_description, menu_lg
from ..config import WINDOW_WIDTH, ASSETS_FOLDER, WINDOW_HEIGHT
from ..components import Button, Text

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .render import MenuRender

from ..enums import MenuPage


class MenuHowToPlay:
    def __init__(self, menu: 'MenuRender') -> None:
        self.menu = menu
        # self.background = pygame.image.load(f"{ASSETS_FOLDER}/menu-background-nologo.jpg")
        # self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.margin_x = 10
        self.margin_top = 20
        self.surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.blackboard_sprite = pygame.image.load(f"{ASSETS_FOLDER}/images/blackboard.png")
        self.blackboard_sprite = pygame.transform.scale(self.blackboard_sprite, (WINDOW_WIDTH, 500))

        self.background_sprite = pygame.image.load(f"{ASSETS_FOLDER}/images/how-to-play-background.png")
        self.background_scale = 4 * 64
        self.background_sprite = pygame.transform.scale(self.background_sprite, (self.background_scale, self.background_scale))

        self.how_to_play_description = "O seu objetivo no jogo é colar na prova sem ser pego no flagra pelo professor. O professor anda atenciosamente pela sala durante a prova procurando alunos como VOCÊ para reprovar sem pensar duas vezes. Use [Ctrl + C] para abrir a cola, e caso perceba que o professor está se aproximando use [Esc] para esconder a cola rapidamente. Se você for visto com a cola aberta você perde. Para ganhar escreva o texto da cola na esquerda para a prova que está na direita. Obs: o texto escrito na prova precisa estar IDÊNTICO ao da cola para que o jogo seja ganho."

    def render(self):
        self.render_background()
        # self.menu.app.surface.blit(self.background, (0, 0))
        self.surface.blit(self.blackboard_sprite, (0, self.margin_top))

        Text(surface=self.surface,
            content=self.how_to_play_description,
            color=pygame.Color(255, 255, 255),
            position=(self.margin_x + 60, 60),
            font=menu_how_to_play_description,
            line_max_width=self.blackboard_sprite.get_width() - 140,
            line_spacing=14)


        self.menu.app.surface.blit(self.surface, (0, 0))
        Button(surface=self.menu.app.surface,
            label='VOLTAR', 
            label_font=menu_lg,
            rect=pygame.Rect(WINDOW_WIDTH // 2 - self.menu.buttons_width // 2, 560, self.menu.buttons_width, 50),
            on_click=self.onclick_back,
            event_list=self.menu.app.event_list)
        
    def onclick_back(self):
        self.menu.active_page = MenuPage.MAIN
        self.menu.button_back_fx.play()

    def render_background(self):
        for x in range(0, WINDOW_WIDTH, self.background_scale):
            for y in range(0, WINDOW_HEIGHT, self.background_scale):
                self.surface.blit(self.background_sprite, (x, y))