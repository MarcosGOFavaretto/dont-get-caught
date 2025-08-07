import pygame
from ..ui.utils import show_error_toast
from ..config import THEME_UI_FILE, WINDOW_HEIGHT, WINDOW_WIDTH, ASSETS_FOLDER
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..app import App

import pygame_gui
from ..service import service_utils, user_service

class SignupRender:
    def __init__(self, app: 'App'):
        self.app = app
        self.ui_manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT), theme_path=THEME_UI_FILE)
        self.background = pygame.image.load(f"{ASSETS_FOLDER}/images/menu-background-nologo.jpg")
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH + 60, WINDOW_HEIGHT))
        self.overlay_surface = pygame.Surface((WINDOW_WIDTH + 60, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.toast_error_rect = pygame.Rect((WINDOW_WIDTH // 2 - 300 // 2, WINDOW_HEIGHT // 2 - 30 // 2), (300, 30))
        self.define_form_ui_components()

    def submit_signup(self):
        username = self.username_input.get_text()
        email = self.email_input.get_text()
        password = self.password_input.get_text()
        password_confirmation = self.password_confirmation_input.get_text()

        # validating form
        if username == '':
            show_error_toast(self.ui_manager, "O campo username é obrigatório")
            return
        
        if email == '':
            show_error_toast(self.ui_manager, "O campo e-mail é obrigatório")
            return
        
        if password == '':
            show_error_toast(self.ui_manager, "O campo senha é obrigatório")
            return
        
        if password != password_confirmation:
            show_error_toast(self.ui_manager, "As senhas não coincidem")
            return
        
        try:
            response = user_service.create(username, email, password)
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
                if event.ui_element == self.create_account_button:
                    self.submit_signup()
                if event.ui_element == self.login_button:
                    self.app.go_to_login()

            self.ui_manager.process_events(event)


        self.ui_manager.update(self.app.time_delta)
        self.ui_manager.draw_ui(self.app.surface)

    def define_form_ui_components(self):
        input_width = 300
        input_height = 50
        input_x = (WINDOW_WIDTH - input_width) // 2

        label_height = 25
        input_spacing = 80
        form_y_initial = 120

        button_spacing = 60


        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((input_x - (input_width//2) + 37, form_y_initial + 0 * input_spacing - label_height), (input_width, label_height)),
            text="Username",
            object_id="#login_label",
            manager=self.ui_manager
        )

        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((input_x - (input_width//2) + 25, form_y_initial + 1 * input_spacing - label_height), (input_width, label_height)),
            text="E-mail",
            object_id="#login_label",
            manager=self.ui_manager
        )

        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((input_x - (input_width//2) + 25, form_y_initial + 2 * input_spacing - label_height), (input_width, label_height)),
            text="Senha",
            object_id="#login_label",
            manager=self.ui_manager
        )

        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((input_x - (input_width//2) + 60, form_y_initial + 3 * input_spacing - label_height), (input_width, label_height)),
            text="Confirmar senha",
            object_id="#login_label",
            manager=self.ui_manager
        )

        # Create input fields

        self.username_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((input_x, form_y_initial + 0 * input_spacing), (input_width, input_height)),
            manager=self.ui_manager,
            object_id="#login_input"
        )

        self.email_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((input_x, form_y_initial + 1 * input_spacing), (input_width, input_height)),
            manager=self.ui_manager,
            object_id="#login_input"
        )

        self.password_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((input_x, form_y_initial + 2 * input_spacing), (input_width, input_height)),
            manager=self.ui_manager,
            object_id="#login_input"
        )
        self.password_input.set_text_hidden(True)  # hides password input

        self.password_confirmation_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((input_x, form_y_initial + 3 * input_spacing), (input_width, input_height)),
            manager=self.ui_manager,
            object_id="#login_input"
        )
        self.password_confirmation_input.set_text_hidden(True)  # hides password input

        # BUTTONS

        self.create_account_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((input_x, form_y_initial + 4 * input_spacing + button_spacing * 0), (input_width, 40)),
            text='Criar Conta',
            manager=self.ui_manager,
            object_id='#button_auth'
        )
    
        self.login_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((input_x, form_y_initial + 4 * input_spacing + button_spacing * 1), (input_width, 40)),
            text='Fazer Login',
            manager=self.ui_manager,
            object_id='#button_auth'
        )

