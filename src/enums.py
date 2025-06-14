from enum import Enum

class GameLevels(Enum):
    EASY = 'EASY'
    MEDIUM = 'MEDIUM'
    HARD = 'HARD'

class MenuPage(Enum):
    MAIN = 'MAIN'
    GAME_LEVELS = 'GAME_LEVELS'
    HOW_TO_PLAY = 'HOW_TO_PLAY'

class GameOverReason(Enum):
    TIME_OVER = 'TIME_OVER'
    CAUGHTED = 'CAUGHTED'