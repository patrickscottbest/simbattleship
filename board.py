import random
from typing import List, Tuple, Dict
from enums import CellState, ShotResult

class Ship:
    def __init__(self, name: str, length: int):
        self.name = name
        self.length = length
        self.hits = 0

    @property
    def is_sunk(self) -> bool:
        return self.hits >= self.length

class Board:
    SIZE = 10

    def __init__(self):
        # 10x10 grid initialized to EMPTY
        self.grid = [[CellState.EMPTY for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.ships: List[Ship] = []
        self.ship_map: Dict[Tuple[int, int], Ship] = {} # Maps coordinates to Ship objects
        self.shots_received = set()

    def place_ships_randomly(self):
        """Places the standard 5 battleship fleet randomly."""
        fleet = [
            Ship("Carrier", 5),
            Ship("Battleship", 4),
            Ship("Cruiser", 3),
            Ship("Submarine", 3),
            Ship("Destroyer", 2)
        ]
        
        for ship in fleet:
            placed = False
            attempts = 0
            while not placed and attempts < 1000:
                x = random.randint(0, self.SIZE - 1)
                y = random.randint(0, self.SIZE - 1)
                horizontal = random.choice([True, False])
                if self._can_place(ship, x, y, horizontal):
                    self._place(ship, x, y, horizontal)
                    placed = True
                attempts += 1
            if not placed:
                raise RuntimeError(f"Failed to place {ship.name} after 1000 attempts.")

    def _can_place(self, ship: Ship, x: int, y: int, horizontal: bool) -> bool:
        for i in range(ship.length):
            cx, cy = (x + i, y) if horizontal else (x, y + i)
            if cx >= self.SIZE or cy >= self.SIZE:
                return False
            if self.grid[cy][cx] != CellState.EMPTY:
                return False
        return True

    def _place(self, ship: Ship, x: int, y: int, horizontal: bool):
        self.ships.append(ship)
        for i in range(ship.length):
            cx, cy = (x + i, y) if horizontal else (x, y + i)
            self.grid[cy][cx] = CellState.SHIP
            self.ship_map[(cx, cy)] = ship

    def receive_shot(self, x: int, y: int) -> ShotResult:
        if not (0 <= x < self.SIZE and 0 <= y < self.SIZE):
            return ShotResult.DUPLICATE # Treat OOB as wasted shot
        
        if (x, y) in self.shots_received:
            return ShotResult.DUPLICATE

        self.shots_received.add((x, y))
        cell = self.grid[y][x]

        if cell == CellState.EMPTY:
            self.grid[y][x] = CellState.MISS
            return ShotResult.MISS
        
        elif cell == CellState.SHIP:
            self.grid[y][x] = CellState.HIT
            ship = self.ship_map[(x, y)]
            ship.hits += 1
            if ship.is_sunk:
                return ShotResult.SUNK
            return ShotResult.HIT
            
        return ShotResult.DUPLICATE

    def all_ships_sunk(self) -> bool:
        return all(ship.is_sunk for ship in self.ships)