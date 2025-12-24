from player import RandomPlayer, HuntTargetPlayer, HuntTargetPlayerMore
from game import Game
from visualizer import show_game_state, InteractiveVisualizer, get_player_selection
import argparse
import time

def run_simulation(p1_class, p2_class, iterations=1, visualize=False):
    p1_wins = 0
    p2_wins = 0
    total_turns = 0

    print(f"Starting simulation: {p1_class.__name__} vs {p2_class.__name__}")
    print(f"Iterations: {iterations}")

    start_time = time.time()

    vis = None
    if visualize:
        vis = InteractiveVisualizer()

    for i in range(iterations):
        # Instantiate fresh players for every game
        p1 = p1_class(p1_class.__name__)
        p2 = p2_class(p2_class.__name__)
        
        game = Game(p1, p2)
        observer = (lambda p1, p2, turn: vis.update(p1, p2, i + 1, turn)) if vis else None
        winner = game.play(observer=observer)
        
        if vis:
            vis.show_round_result(p1, p2, i + 1, winner.name)
        
        total_turns += game.turn_count
        if winner == p1:
            p1_wins += 1
        else:
            p2_wins += 1

    if vis:
        vis.close()

    elapsed = time.time() - start_time
    avg_turns = total_turns / iterations

    print("-" * 30)
    print(f"Results ({elapsed:.2f}s):")
    print(f"{p1_class.__name__} Wins: {p1_wins} ({p1_wins/iterations:.1%})")
    print(f"{p2_class.__name__} Wins: {p2_wins} ({p2_wins/iterations:.1%})")
    print(f"Average Turns per Game: {avg_turns:.1f}")
    print("-" * 30)
    
    if iterations > 0:
        print("Displaying final game state...")
        show_game_state(p1, p2, winner.name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Battleship simulation")
    parser.add_argument("-n", "--iterations", type=int, default=1000, help="Number of iterations to run")
    parser.add_argument("-v", "--visualize", default=True, action="store_true", help="Visual play-by-play (press space to advance)")
    args = parser.parse_args()

    p1_class = HuntTargetPlayer
    p2_class = HuntTargetPlayerMore

    if args.visualize:
        classes = [RandomPlayer, HuntTargetPlayer, HuntTargetPlayerMore]
        descriptions = {
            RandomPlayer: "Fires randomly at any valid coordinate.",
            HuntTargetPlayer: "Hunts by checking gaps for smallest ship. Targets neighbors upon hit.",
            HuntTargetPlayerMore: "Hunts by maximizing distance from previous shots. Targets neighbors upon hit."
        }
        p1_class, p2_class = get_player_selection(classes, descriptions)

    # Compare Random Strategy vs Hunt/Target Strategy
    run_simulation(p1_class, p2_class, iterations=args.iterations, visualize=args.visualize)