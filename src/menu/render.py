import pygame
from ..fonts import merriweather_large as menu_font
from ..config import WINDOW_HEIGHT, WINDOW_WIDTH, ASSETS_FOLDER

class MenuRender:
    def __init__(self, app):
        self.app = app
        self.background = pygame.image.load(f"{ASSETS_FOLDER}/menu-background.png")
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.buttons_width = 260
        self.background_sound = pygame.mixer.Sound(f'{ASSETS_FOLDER}/background-sound-menu.mp3')
        self.background_sound.play(loops=-1, fade_ms=2000)
        self.background_sound.set_volume(0.2)

        self.button_click_fx = pygame.mixer.Sound(f'{ASSETS_FOLDER}/menu-click-btn.mp3')
        self.button_back_fx = pygame.mixer.Sound(f'{ASSETS_FOLDER}/menu-back-btn.mp3')

        self.button_click_fx.set_volume(0.5)
        self.button_back_fx.set_volume(0.5)

        self.menu_options = [
            {"text": "INICIAR", "rect": pygame.Rect(WINDOW_WIDTH // 2 - self.buttons_width // 2, 260, self.buttons_width, 50)},
            {"text": "OPÇOES", "rect": pygame.Rect(WINDOW_WIDTH // 2 - self.buttons_width // 2, 340, self.buttons_width, 50)},
            {"text": "SAIR", "rect": pygame.Rect(WINDOW_WIDTH // 2 - self.buttons_width // 2, 420, self.buttons_width, 50)}
        ]

        self.menu_levels = [
            {"text": "FACIL", "rect": pygame.Rect(WINDOW_WIDTH // 2 - self.buttons_width // 2, 260, self.buttons_width, 50)},
            {"text": "MEDIO", "rect": pygame.Rect(WINDOW_WIDTH // 2 - self.buttons_width // 2, 340, self.buttons_width, 50)},
            {"text": "DIFICIL", "rect": pygame.Rect(WINDOW_WIDTH // 2 - self.buttons_width // 2, 420, self.buttons_width, 50)}
        ]

        self.back_button = {"text": "VOLTAR", "rect": pygame.Rect(WINDOW_WIDTH // 2 - self.buttons_width // 2, 500, self.buttons_width, 50)}

        self.button_mouse = 150  #Transparência do botão aumenta ao passar o mouse sobre ele

        self.menu_active = True
        self.difficulty_menu_active = False

    def render(self):
        self.app.surface.blit(self.background, (0, 0))

        if self.menu_active:
            self.draw_buttons(self.menu_options)
        elif self.difficulty_menu_active:
            self.draw_buttons(self.menu_levels)
            self.draw_text_with_outline(self.back_button["text"], menu_font, (0, 0, 0), (255, 255, 255), self.back_button["rect"].center)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.menu_active:
                    for button in self.menu_options:
                        if button["rect"].collidepoint(event.pos):
                            if button["text"] == "INICIAR":
                                self.button_click_fx.play()
                                self.menu_active = False
                                self.difficulty_menu_active = True
                            elif button["text"] == "SAIR":
                                pygame.quit()
                                exit()
                elif self.difficulty_menu_active:
                    for button in self.menu_levels:
                        if button["rect"].collidepoint(event.pos):
                            self.button_click_fx.play()
                            self.app.start_game()
                            # print(f"Dificuldade selecionada: {button['text']}")
                    if self.back_button["rect"].collidepoint(event.pos):
                        self.button_back_fx.play()
                        self.menu_active = True
                        self.difficulty_menu_active = False

    def draw_text_with_outline(self, text, font, text_color, outline_color, position):
        textsurface = font.render(text, True, text_color)
        outlinesurface = font.render(text, True, outline_color)
        textrect = textsurface.get_rect(center=position)
        offsets = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        for dx, dy in offsets:
            self.app.surface.blit(outlinesurface, (textrect.x + dx, textrect.y + dy))
        self.app.surface.blit(textsurface, textrect.topleft)

    def draw_buttons(self, button_list):
        mouse_pos = pygame.mouse.get_pos() #Pega a posição do mouse

        #'for' usado para detectar se o mouse está sobre o botão
        for button in button_list:
            is_hovered = button["rect"].collidepoint(mouse_pos)
            btnmouse = self.button_mouse if is_hovered else 100  #Se passar o mouse no botão, diminui a transparência dele
            
            surfacebtn = pygame.Surface((button["rect"].width, button["rect"].height), pygame.SRCALPHA)
            surfacebtn.fill((255, 255, 255, btnmouse))
            self.app.surface.blit(surfacebtn, button["rect"].topleft)
            
            self.draw_text_with_outline(button["text"], menu_font, (0, 0, 0), (255, 255, 255), button["rect"].center)        
