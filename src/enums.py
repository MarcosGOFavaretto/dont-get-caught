from enum import Enum

class Screens(Enum):
    MENU = 'MENU'
    GAME_RUNTIME = 'GAME_RUNTIME'
    SETTINGS = 'SETTINGS'
    CREDITS = 'CREDITS'
    COLA = 'COLA'

class GameLevels(Enum):
    EASY = 'EASY'
    MEDIUM = 'MEDIUM'
    HARD = 'HARD'