import pygame
from ..fonts import menu_lg
from ..config import FPS, WINDOW_HEIGHT, WINDOW_WIDTH, ASSETS_FOLDER
from ..components import Button

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..app import App

from ..enums import MenuPage

import pygame_gui

class AuthRender:
    def __init__(self, app: 'App'):
        self.app = app
        self.background = pygame.image.load(f"{ASSETS_FOLDER}/images/menu-background-nologo.jpg")
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH + 60, WINDOW_HEIGHT))
        self.overlay_surface = pygame.Surface((WINDOW_WIDTH + 60, WINDOW_HEIGHT), pygame.SRCALPHA)

        input_width = 300
        input_height = 50
        input_x = (WINDOW_WIDTH - input_width) // 2

        label_height = 25

        # Labels
        self.username_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((input_x - (input_width//2) + 37, 140 - label_height), (input_width, label_height)),
            text="Username",
            object_id="#login_label",
            manager=self.app.ui_manager
        )

        self.password_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((input_x - (input_width//2) + 35, 220 - label_height), (input_width, label_height)),
            text="Password",
            object_id="#login_label",
            manager=self.app.ui_manager
        )

        # Create input fields and button
        self.username_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((input_x, 140), (input_width, input_height)),
            manager=self.app.ui_manager,
            object_id="#login_input"
        )
        self.username_input.set_text('')

        self.password_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((input_x, 220), (input_width, input_height)),
            manager=self.app.ui_manager,
            object_id="#login_input"
        )
        self.password_input.set_text('')
        self.password_input.set_text_hidden(True)  # hides password input

        self.login_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((input_x, 300), (input_width, 40)),
            text='Login',
            manager=self.app.ui_manager,
        )
    

    def render(self):
        self.app.surface.blit(self.background, (0, 0))
        self.overlay_surface.fill((0, 0, 0, 100))
        self.app.surface.blit(self.overlay_surface, (0, 0))

        for event in self.app.event_list:
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.login_button:
                    username = self.username_input.get_text()
                    password = self.password_input.get_text()
                    print(f"Login attempt: user={username}, pass={password}")

            self.app.ui_manager.process_events(event)


        self.app.ui_manager.update(self.app.time_delta)
        self.app.ui_manager.draw_ui(self.app.surface)
