# Battleship Simulation & Visualizer

A Python-based Battleship game engine designed to simulate and visualize matches between different AI strategies.

## Features

- **Simulation Engine**: Run games to determine the statistical efficiency of different strategies.
- **Interactive Visualizer**: Watch the game unfold turn-by-turn with a GUI built using `tkinter`.
- **Multiple Strategies**: Includes implementations for Random, Hunt/Target, and optimized Hunt/Target algorithms.
- **Performance Metrics**: Tracks win rates and average turns per game.

## Getting Started

### Prerequisites

- Python 3.x
- `tkinter` (Usually included with standard Python installations)

### Installation

Ensure all project files are in the same directory.

## Usage

Run the main script to start the application. By default, this opens a strategy selection menu and then launches the visualizer.

```bash
python main.py
```

### Command Line Arguments

- `-n`, `--iterations`: Number of games to simulate (default: 1000).
- `-v`, `--visualize`: Enable visual play-by-play mode.

### Visualizer Controls

When the visualizer is running, use the following keys to control the playback:

- **Space**: Advance one turn.
- **Enter**: Fast-forward to the end of the current game.
- **A**: Toggle Auto-Play mode.
- **+ / =**: Increase Auto-Play speed.
- **- / _**: Decrease Auto-Play speed.
- **Esc**: Quit the application.

## Strategies

The project includes the following AI implementations:

1.  **RandomPlayer**: Fires at random coordinates.
2.  **HuntTargetPlayer**:
    - **Hunt Mode**: Searches for gaps large enough to fit the smallest remaining ship.
    - **Target Mode**: Upon hitting a ship, targets neighboring cells until the ship is sunk.
3.  **HuntTargetPlayerMore**:
    - **Hunt Mode**: Maximizes distance from previous shots to cover the board efficiently.
    - **Target Mode**: Standard neighbor targeting upon hits.

## Project Structure

- `main.py`: Entry point. Handles argument parsing and simulation loop.
- `game.py`: Manages game logic, turns, and win conditions.
- `board.py`: Handles grid state, ship placement, and shot validation.
- `player.py`: Abstract base class for players and AI strategy implementations.
- `visualizer.py`: `tkinter` GUI for rendering the game state.
- `enums.py`: Common enumerations for cell states and shot results.