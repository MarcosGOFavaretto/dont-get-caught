from ast import PyCF_ALLOW_TOP_LEVEL_AWAIT
import pygame

from ...utils import senoide
from ...timer import Timer, TIME_SECOND
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..render import GameRender
from ...config import ASSETS_FOLDER
from ..teacher.movement import MovementDirection

class CaughtedCutscene():
    def __init__(self, game: 'GameRender'):
        self.game = game
        self.cutscene_time = Timer(wait_time=2 * TIME_SECOND)
        self.render_started = False
        self.teacher_ahh_sound = pygame.mixer.Sound(f'{ASSETS_FOLDER}/sounds/teacher-ahh.mp3')
        self.teacher_exclamation_sprite_down = pygame.image.load(f'{ASSETS_FOLDER}/images/teacher-exclamation.png')
        self.teacher_exclamation_sprite_up = pygame.transform.rotate(self.teacher_exclamation_sprite_down, 180)
        self.teacher_exclamation_sprite_left = pygame.transform.rotate(self.teacher_exclamation_sprite_down, -90)
        self.teacher_exclamation_sprite_right = pygame.transform.rotate(self.teacher_exclamation_sprite_left, 180)

        self.exclamation_state_map = {
            MovementDirection.DOWN: dict(offset=(0, - 26), sprite=self.teacher_exclamation_sprite_down),
            MovementDirection.UP: dict(offset=(0, 26), sprite=self.teacher_exclamation_sprite_up),
            MovementDirection.LEFT: dict(offset=(26, 0), sprite=self.teacher_exclamation_sprite_left),
            MovementDirection.RIGHT: dict(offset=(-26, 0), sprite=self.teacher_exclamation_sprite_right)
        }

    def setup(self):
        self.cutscene_time.start()
        self.teacher_ahh_sound.play()
        self.render_started = True

    def render(self, on_ends):
        if not self.render_started:
            self.setup()
            return
        
        if self.cutscene_time.time_is_up():
            self.teacher_ahh_sound.stop()
            on_ends()
            return
        

        exclamation_state = self.exclamation_state_map[self.game.teacher.direction]
        offset_x, offset_y = exclamation_state.get('offset')
        self.game.app.surface.blit(exclamation_state.get('sprite'), (self.game.teacher.position.x - 32 + offset_x, self.game.teacher.position.y - 32 + offset_y))
        
        



        
