from enum import Enum

class CellState(Enum):
    EMPTY = 0
    SHIP = 1
    MISS = 2
    HIT = 3
    SUNK = 4

class ShotResult(Enum):
    MISS = "Miss"
    HIT = "Hit"
    SUNK = "Sunk"
    DUPLICATE = "Duplicate"
    GAME_OVER = "Game Over"