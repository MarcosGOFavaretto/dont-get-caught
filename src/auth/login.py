import pygame
from ..service import service_utils, user_service
from ..config import WINDOW_HEIGHT, WINDOW_WIDTH, ASSETS_FOLDER
from ..ui.utils import show_error_toast
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..app import App

import pygame_gui

class LoginRender:
    def __init__(self, app: 'App'):
        self.app = app
        self.ui_manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT), theme_path='./src/ui/theme.json')
        self.background = pygame.image.load(f"{ASSETS_FOLDER}/images/menu-background-nologo.jpg")
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.overlay_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.define_form_ui_components()

    def submit_login(self):
        email = self.email_input.get_text()
        password = self.password_input.get_text()

        # validating form
        if email == '':
            show_error_toast(self.ui_manager, "O campo e-mail é obrigatório")
            return
        
        if password == '':
            show_error_toast(self.ui_manager, "O campo senha é obrigatório")
            return
        
        try:
            response = user_service.login(email, password)
            service_utils.store_access_token(response['token'])
            self.app.go_to_menu()
        except service_utils.ServiceError as se:
            show_error_toast(self.ui_manager, se.get_translated_message())
            return

    def render(self):
        self.app.surface.blit(self.background, (0, 0))
        self.overlay_surface.fill((0, 0, 0, 100))
        self.app.surface.blit(self.overlay_surface, (0, 0))

        for event in self.app.event_list:
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.login_button:
                    self.submit_login()
                if event.ui_element == self.signup_button:
                    self.app.go_to_signup()

            self.ui_manager.process_events(event)


        self.ui_manager.update(self.app.time_delta)
        self.ui_manager.draw_ui(self.app.surface)

    def define_form_ui_components(self):
        input_width = 300
        input_height = 50
        input_x = (WINDOW_WIDTH - input_width) // 2
        label_height = 25
    
        # Labels
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((input_x - (input_width//2) + 25, 140 - label_height), (input_width, label_height)),
            text="E-mail",
            object_id="#login_label",
            manager=self.ui_manager
        )

        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((input_x - (input_width//2) + 25, 220 - label_height), (input_width, label_height)),
            text="Senha",
            object_id="#login_label",
            manager=self.ui_manager
        )

        # Create input fields

        self.email_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((input_x, 140), (input_width, input_height)),
            manager=self.ui_manager,
            object_id="#login_input"
        )
        self.email_input.set_text('')

        self.password_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((input_x, 220), (input_width, input_height)),
            manager=self.ui_manager,
            object_id="#login_input"
        )
        self.password_input.set_text('')
        self.password_input.set_text_hidden(True)  # hides password input

        # Buttons

        self.login_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((input_x, 300), (input_width, 40)),
            text='Login',
            manager=self.ui_manager,
            object_id='#button_auth'
        )
    
        self.signup_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((input_x, 360), (input_width, 40)),
            text='Criar conta',
            manager=self.ui_manager,
            object_id='#button_auth'
        )
