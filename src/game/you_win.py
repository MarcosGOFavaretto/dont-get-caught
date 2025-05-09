from ..config import WINDOW_HEIGHT, WINDOW_WIDTH, ASSETS_FOLDER
import pygame
from ..components import Button, Text
from .. import fonts
from ..timer import Timer, TIME_SECOND
import random
from ..animations import Confetti

class YouWin:
    def __init__(self, game):
        self.game = game
        self.surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.darken_animation_timer = Timer(wait_time=0.5 * TIME_SECOND)
        self.darken_animation_timer.start()
        self.screen_opacity = 0
        self.winning_hehe = pygame.mixer.Sound(f'{ASSETS_FOLDER}/winning-hehe.mp3')
        self.winning_hehe.set_volume(0.1)
        self.winning_hehe.play(loops=-1, fade_ms=4 * TIME_SECOND)
        self.winning_song = pygame.mixer.Sound(f'{ASSETS_FOLDER}/winning-song.mp3')
        self.winning_song.set_volume(0.4)
        self.winning_song.play()

        self.congratulations_phrases = [
            "Parabéns, você colou como um mestre!",
            "Ninguém engana o professor como você!",
            "Você passou com louvor… e um pouco de trapaça!",
            "Mestre da arte da cola! Respeito!",
            "Você merece um diploma honorário em estratégias clandestinas!",
            "A cola nunca foi tão bem aplicada!",
            "Você burlou o sistema como um verdadeiro gênio!",
            "Sua inteligência (e astúcia) brilharam hoje!",
            "O professor nunca teve chance contra você!",
            "Vitória merecida! Mas não conte pra ninguém..."
        ]

        self.subtext = random.choice(self.congratulations_phrases)

        self.confetti_list = [Confetti(height=WINDOW_HEIGHT, width=WINDOW_WIDTH) for _ in range(100)]

    def render(self):
        self.fade_in_animation(start=0, end=250, velocity=10)

        self.surface.fill((0, 0, 0, self.screen_opacity))

        for confetti in self.confetti_list:
            confetti.update()
            confetti.draw(self.surface)

        Text(surface=self.surface,
                content='YOU WIN',
                color=(255, 255, 255, self.screen_opacity),
                position=(WINDOW_WIDTH // 2, 200),
                font=fonts.game_final_screen_title,
                outline_color=(0, 0, 0),
                outline_size=3)
        
        Text(surface=self.surface,
                content=self.subtext,
                color=(255, 255, 255, self.screen_opacity),
                position=(WINDOW_WIDTH // 2, 280),
                font=fonts.game_final_subtext,
                outline_color=(0, 0, 0),
                outline_size=1)

        Button(surface=self.surface,
                label='Jogar novamente', 
                label_font=fonts.game_final_btn_label,
                background_color=(255, 255, 255),
                rect=pygame.Rect(WINDOW_WIDTH // 2 - 300 // 2, 340, 300, 50),
                on_click=self.play_again)
        
        Button(surface=self.surface,
                label='Ir para o Menu', 
                label_font=fonts.game_final_btn_label,
                background_color=(255, 255, 255),
                rect=pygame.Rect(WINDOW_WIDTH // 2 - 300 // 2, 420, 300, 50), 
                on_click=self.go_to_menu)

        self.game.app.surface.blit(self.surface, (0, 0))      

    def go_to_menu(self):
        self.game.app.open_menu()
        self.winning_hehe.stop()
        self.winning_song.stop()

    def play_again(self):
        self.game.app.start_game()
        self.winning_hehe.stop()
        self.winning_song.stop()

    def fade_in_animation(self, start: int, end: int, velocity: int = 1):
        if self.screen_opacity + velocity < end:
            self.screen_opacity += start + velocity