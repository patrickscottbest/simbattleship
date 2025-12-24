import random
from abc import ABC, abstractmethod
from typing import Tuple, Set, List, Optional
from board import Board
from enums import ShotResult

class Player(ABC):
    def __init__(self, name: str):
        self.name = name
        self.board = Board()
        self.shots_fired: Set[Tuple[int, int]] = set()

    def setup_board(self):
        """Strategies could override this to place ships intelligently."""
        self.board.place_ships_randomly()

    def random_probe(self) -> Tuple[int, int]:
        while True:
            x = random.randint(0, Board.SIZE - 1)
            y = random.randint(0, Board.SIZE - 1)
            if (x, y) not in self.shots_fired:
                return x, y

    def min_length_probe(self) -> Tuple[int, int]:
        candidates = []
        min_len = 2 # Smallest ship length
        
        for x in range(Board.SIZE):
            for y in range(Board.SIZE):
                if (x, y) in self.shots_fired:
                    continue
                
                # Check Horizontal fit
                h_fit = False
                for start_x in range(max(0, x - min_len + 1), min(Board.SIZE - min_len + 1, x + 1)):
                    if all((cx, y) not in self.shots_fired for cx in range(start_x, start_x + min_len)):
                        h_fit = True
                        break
                
                # Check Vertical fit
                v_fit = False
                if not h_fit:
                    for start_y in range(max(0, y - min_len + 1), min(Board.SIZE - min_len + 1, y + 1)):
                        if all((x, cy) not in self.shots_fired for cy in range(start_y, start_y + min_len)):
                            v_fit = True
                            break
                
                if h_fit or v_fit:
                    candidates.append((x, y))
        
        if candidates:
            return random.choice(candidates)
        return self.random_probe()

    @abstractmethod
    def get_shot(self) -> Tuple[int, int]:
        """Determine coordinates for the next shot."""
        pass

    @abstractmethod
    def inform_result(self, x: int, y: int, result: ShotResult):
        """Update internal state based on the result of the shot."""
        pass

class RandomPlayer(Player):
    def get_shot(self) -> Tuple[int, int]:
        x, y = self.random_probe()
        self.shots_fired.add((x, y))
        return x, y

    def inform_result(self, x: int, y: int, result: ShotResult):
        # Random player doesn't care about results
        pass

class HuntTargetPlayer(Player):
    """
    Hunt Mode: Fire randomly.
    Target Mode: If a hit is recorded, add neighbors to a stack and fire at them.
    """
    def __init__(self, name: str):
        super().__init__(name)
        self.target_stack: List[Tuple[int, int]] = []
        self.last_hit: Optional[Tuple[int, int]] = None

    def get_shot(self) -> Tuple[int, int]:
        # Target Mode
        while self.target_stack:
            x, y = self.target_stack.pop()
            if (x, y) not in self.shots_fired:
                self.shots_fired.add((x, y))
                return x, y
        
        # Hunt Mode
        x, y = self.min_length_probe()
        self.shots_fired.add((x, y))
        return x, y

    def inform_result(self, x: int, y: int, result: ShotResult):
        if result == ShotResult.HIT:
            if self.last_hit and (abs(x - self.last_hit[0]) + abs(y - self.last_hit[1]) == 1):
                dx = x - self.last_hit[0]
                dy = y - self.last_hit[1]
                nx, ny = x + dx, y + dy
                if 0 <= nx < Board.SIZE and 0 <= ny < Board.SIZE:
                    if (nx, ny) not in self.shots_fired:
                        self.target_stack.append((nx, ny))
            else:
                self._add_neighbors(x, y)
            self.last_hit = (x, y)
        elif result == ShotResult.SUNK:
            self.last_hit = None

    def _add_neighbors(self, x: int, y: int):
        neighbors = [
            (x, y - 1), (x, y + 1),
            (x - 1, y), (x + 1, y)
        ]
        for nx, ny in neighbors:
            if 0 <= nx < Board.SIZE and 0 <= ny < Board.SIZE:
                if (nx, ny) not in self.shots_fired:
                    self.target_stack.append((nx, ny))

class HuntTargetPlayerMore(Player):
    """
    Hunt Mode: Fire randomly.
    Target Mode: If a hit is recorded, add neighbors to a stack and fire at them.
    """
    def __init__(self, name: str):
        super().__init__(name)
        self.target_stack: List[Tuple[int, int]] = []
        self.last_hit: Optional[Tuple[int, int]] = None

    def get_shot(self) -> Tuple[int, int]:
        # Target Mode
        while self.target_stack:
            x, y = self.target_stack.pop()
            if (x, y) not in self.shots_fired:
                self.shots_fired.add((x, y))
                return x, y
        
        # Hunt Mode
        x, y = self.max_distance_probe()
        self.shots_fired.add((x, y))
        return x, y

    def inform_result(self, x: int, y: int, result: ShotResult):
        if result == ShotResult.HIT:
            if self.last_hit and (abs(x - self.last_hit[0]) + abs(y - self.last_hit[1]) == 1):
                dx = x - self.last_hit[0]
                dy = y - self.last_hit[1]
                nx, ny = x + dx, y + dy
                if 0 <= nx < Board.SIZE and 0 <= ny < Board.SIZE:
                    if (nx, ny) not in self.shots_fired:
                        self.target_stack.append((nx, ny))
            else:
                self._add_neighbors(x, y)
            self.last_hit = (x, y)
        elif result == ShotResult.SUNK:
            self.last_hit = None

    def _add_neighbors(self, x: int, y: int):
        neighbors = [
            (x, y - 1), (x, y + 1),
            (x - 1, y), (x + 1, y)
        ]
        for nx, ny in neighbors:
            if 0 <= nx < Board.SIZE and 0 <= ny < Board.SIZE:
                if (nx, ny) not in self.shots_fired:
                    self.target_stack.append((nx, ny))

    def max_distance_probe(self) -> Tuple[int, int]:
        if not self.shots_fired:
            return self.random_probe()

        best_candidates = []
        max_min_dist = -1

        for x in range(Board.SIZE):
            for y in range(Board.SIZE):
                if (x, y) in self.shots_fired:
                    continue
                
                # Calculate Manhattan distance to the nearest shot
                current_min_dist = min(abs(x - sx) + abs(y - sy) for sx, sy in self.shots_fired)
                
                if current_min_dist > max_min_dist:
                    max_min_dist = current_min_dist
                    best_candidates = [(x, y)]
                elif current_min_dist == max_min_dist:
                    best_candidates.append((x, y))
        
        if best_candidates:
            return random.choice(best_candidates)
        return self.random_probe()