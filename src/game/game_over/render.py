from ...config import WINDOW_HEIGHT, WINDOW_WIDTH, ASSETS_FOLDER
import pygame
from ...components import Button, Text, RectPosition
from ... import fonts
from ...timer import Timer, TIME_SECOND
import random
from ...animations import Rain
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..render import GameRender
from ...enums import GameOverReason
from .time_over_cutscene import TimeOverCutscene

class GameOverRender:
    def __init__(self, game: 'GameRender', reason: GameOverReason):
        self.game = game
        self.reason = reason
        self.surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.darken_animation_timer = Timer(wait_time=0.5 * TIME_SECOND)
        self.screen_opacity = 0
        self.game_over_sound = pygame.mixer.Sound(f'{ASSETS_FOLDER}/sounds/gameover-trumpet.mp3')
        self.crying_sniffing_sound = pygame.mixer.Sound(f'{ASSETS_FOLDER}/sounds/crying-sniffing.mp3')
        self.crying_sniffing_sound.set_volume(0.4)
        self.cutscene_render = TimeOverCutscene(game=self.game)
        self.cutscene_ends = False
        self.overlay_started = False

        self.phrases = [
            "Nem colando conseguiu? Aí complicou, hein...",
            "Se cola fosse superpoder, você ainda seria um estagiário.",
            "Já pensou em estudar? Talvez ajude na próxima!",
            "O professor venceu... de novo. Quer tentar com a apostila aberta?",
            "Você falhou com estilo. Pena que estilo não dá ponto.",
            "Foi mal... o plano era bom. Só faltou funcionar.",
            "Até os gênios erram. Tente de novo!",
            "Se seu objetivo era perder, parabéns: missão cumprida!",
            "Respira fundo… e mostra do que você é capaz na próxima!",
            "Você não falhou, apenas descobriu uma forma que não funciona!"
        ]

        self.subtext = random.choice(self.phrases)

        self.rain_list = [Rain(height=WINDOW_HEIGHT, width=WINDOW_WIDTH) for _ in range(100)]

    def render(self):
        if self.cutscene_ends:
            self.render_overlay()
            return
        self.cutscene_render.render(on_ends=self.on_ends_cutscene)

    def on_ends_cutscene(self):
        self.cutscene_ends = True

    def setup_overlay(self):
        self.game_over_sound.play()
        self.darken_animation_timer.start()
        self.crying_sniffing_sound.play(loops=-1, fade_ms=1 * TIME_SECOND)
        self.overlay_started = True

    def render_overlay(self):
        if not self.overlay_started:
            self.setup_overlay()

        self.fade_in_animation(start=0, end=220, velocity=10)

        self.surface.fill((0, 0, 0, self.screen_opacity))

        for rain in self.rain_list:
            rain.update()
            rain.draw(self.surface)

        Text(surface=self.surface,
                content='GAME OVER',
                color=pygame.Color(255, 255, 255, self.screen_opacity),
                position=(WINDOW_WIDTH // 2, 200),
                font=fonts.game_final_screen_title,
                outline_color=pygame.Color(0, 0, 0),
                outline_size=3,
                rect_pos=RectPosition.CENTER)
        
        Text(surface=self.surface,
                content=self.subtext,
                color=pygame.Color(255, 255, 255, self.screen_opacity),
                position=(WINDOW_WIDTH // 2, 280),
                font=fonts.game_final_subtext,
                outline_color=pygame.Color(0, 0, 0),
                outline_size=1,
                rect_pos=RectPosition.CENTER)

        Button(surface=self.surface,
                label='Jogar novamente', 
                label_font=fonts.game_final_btn_label,
                background_color=pygame.Color(255, 255, 255),
                rect=pygame.Rect(WINDOW_WIDTH // 2 - 300 // 2, 340, 300, 50),
                on_click=self.play_again,
                event_list=self.game.app.event_list)
        
        Button(surface=self.surface,
                label='Ir para o Menu', 
                label_font=fonts.game_final_btn_label,
                background_color=pygame.Color(255, 255, 255),
                rect=pygame.Rect(WINDOW_WIDTH // 2 - 300 // 2, 420, 300, 50), 
                on_click=self.go_to_menu,
                event_list=self.game.app.event_list)

        self.game.app.surface.blit(self.surface, (0, 0))      

    def go_to_menu(self):
        self.game.app.open_menu()
        self.crying_sniffing_sound.stop()

    def play_again(self):
        self.game.app.start_game(self.game.selected_level)
        self.crying_sniffing_sound.stop()

    def fade_in_animation(self, start: int, end: int, velocity: int = 1):
        if self.screen_opacity + velocity < end:
            self.screen_opacity += start + velocity