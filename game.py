from player import Player
from enums import ShotResult

class Game:
    def __init__(self, player1: Player, player2: Player):
        self.p1 = player1
        self.p2 = player2
        self.turn_count = 0

    def play(self, observer=None) -> Player:
        """
        Runs the game loop until a winner is decided.
        Returns the winning Player object.
        """
        self.p1.setup_board()
        self.p2.setup_board()

        current = self.p1
        opponent = self.p2

        while True:
            self.turn_count += 1
            
            # Get shot coordinates from current player
            x, y = current.get_shot()
            
            # Process shot on opponent's board
            result = opponent.board.receive_shot(x, y)
            
            # Inform current player of the result (to update strategy)
            current.inform_result(x, y, result)

            if observer:
                observer(self.p1, self.p2, self.turn_count)

            if opponent.board.all_ships_sunk():
                return current

            # Swap turns
            current, opponent = opponent, current