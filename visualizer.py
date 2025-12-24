import tkinter as tk
import time
import sys
from enums import CellState

def draw_board(canvas, board, offset_x, offset_y, cell_size, player_name):
    # Draw Player Name
    canvas.create_text(offset_x + (10 * cell_size) / 2, offset_y - 20, 
                       text=player_name, font=("Arial", 14, "bold"))

    for y in range(10):
        for x in range(10):
            x0 = offset_x + x * cell_size
            y0 = offset_y + y * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size

            cell = board.grid[y][x]
            
            fill_color = "lightblue" # Empty/Water
            
            if cell == CellState.MISS:
                fill_color = "white"
            elif cell == CellState.SHIP:
                fill_color = "gray"
            elif cell == CellState.HIT:
                # Check if the ship at this location is sunk
                if (x, y) in board.ship_map and board.ship_map[(x, y)].is_sunk:
                    fill_color = "#d32f2f" # Red (Sunk)
                else:
                    fill_color = "orange" # Hit

            canvas.create_rectangle(x0, y0, x1, y1, fill=fill_color, outline="black")
            
            # Draw simple markers for clarity
            if cell == CellState.MISS:
                canvas.create_oval(x0 + 10, y0 + 10, x1 - 10, y1 - 10, outline="black")
            elif cell == CellState.HIT:
                canvas.create_line(x0, y0, x1, y1, fill="black")
                canvas.create_line(x0, y1, x1, y0, fill="black")

def draw_legend(canvas, x, y, size):
    items = [
        ("Water", "lightblue", None),
        ("Ship", "gray", None),
        ("Miss", "white", "oval"),
        ("Hit", "orange", "cross"),
        ("Sunk", "#d32f2f", "cross")
    ]
    
    canvas.create_text(x, y, text="Legend:", font=("Arial", 12, "bold"), anchor="w")
    
    start_x = x + 70
    for label, color, marker in items:
        canvas.create_rectangle(start_x, y - 10, start_x + size, y - 10 + size, fill=color, outline="black")
        if marker == "oval":
            canvas.create_oval(start_x + 4, y - 10 + 4, start_x + size - 4, y - 10 + size - 4, outline="black")
        elif marker == "cross":
            canvas.create_line(start_x, y - 10, start_x + size, y - 10 + size, fill="black")
            canvas.create_line(start_x, y - 10 + size, start_x + size, y - 10, fill="black")
        canvas.create_text(start_x + size + 5, y, text=label, anchor="w")
        start_x += 90

class InteractiveVisualizer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Battleship Play-by-Play (Press Space to Advance)")
        
        self.cell_size = 30
        self.padding = 70
        self.board_pixel_size = 10 * self.cell_size
        
        window_width = self.padding * 3 + self.board_pixel_size * 2
        window_height = self.padding * 2 + self.board_pixel_size + 80
        
        self.canvas = tk.Canvas(self.root, width=window_width, height=window_height, bg="#f0f0f0")
        self.canvas.pack()
        
        self.advance = False
        self.trigger_enter = False
        self.fast_forward = False
        self.auto_play = False
        self.delay = 0.005

        self.root.bind("<space>", self._on_space)
        self.root.bind("<Return>", self._on_enter)
        self.root.bind("<Escape>", self._on_escape)
        self.root.bind("a", self._on_a)
        self.root.bind("+", self._increase_delay)
        self.root.bind("=", self._increase_delay)
        self.root.bind("-", self._decrease_delay)
        self.root.bind("_", self._decrease_delay)
        self.running = True
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def _on_space(self, event):
        self.advance = True

    def _on_enter(self, event):
        self.trigger_enter = True

    def _on_escape(self, event):
        self.close()
        sys.exit(0)

    def _on_a(self, event):
        self.auto_play = not self.auto_play

    def _increase_delay(self, event):
        if self.delay < 0.0001:
            self.delay = round(self.delay + 0.00001, 5)
        elif self.delay < 0.001:
            self.delay = round(self.delay + 0.0001, 4)
        elif self.delay < 0.050:
            self.delay = round(self.delay + 0.001, 3)
        elif self.delay < 0.500:
            self.delay = round(self.delay + 0.025, 3)

    def _decrease_delay(self, event):
        if self.delay > 0.050001:
            self.delay = round(self.delay - 0.025, 3)
        elif self.delay > 0.001001:
            self.delay = round(self.delay - 0.001, 3)
        elif self.delay > 0.0001001:
            self.delay = round(self.delay - 0.0001, 4)
        elif self.delay > 0.00001001:
            self.delay = round(self.delay - 0.00001, 5)
        else:
            self.delay = 0

    def update(self, p1, p2, iteration, turn):
        if not self.running:
            return

        if self.fast_forward:
            return

        # Optimization: In unlimited mode, skip rendering most frames to speed up
        if self.auto_play and self.delay == 0 and turn % 20 != 0 and turn != 1:
            # Process events to keep UI responsive (e.g. stopping auto-play)
            self.root.update()
            return

        self.canvas.delete("all")
        
        # Display Info
        if self.auto_play:
            delay_info = " | Delay: Unlimited" if self.delay == 0 else f" | Delay: {self.delay * 1000:.2f}ms"
        else:
            delay_info = ""
        info_text = f"Iteration: {iteration} | Turn: {turn}{delay_info}"
        self.canvas.create_text(self.padding, 20, text=info_text, font=("Arial", 16, "bold"), anchor="w")
        
        # Display Options at the bottom
        opts_text = "Options: [Space] Next Turn | [Enter] Finish Game | [A] Auto-Play | [+/-] Speed | [Esc] Quit"
        window_height = int(self.canvas['height'])
        self.canvas.create_text(self.padding, window_height - 20, text=opts_text, font=("Arial", 10), anchor="w")

        # Note: Names are swapped to indicate target board, matching show_game_state logic
        draw_board(self.canvas, p1.board, self.padding, self.padding, self.cell_size, p2.name)
        draw_board(self.canvas, p2.board, self.padding * 2 + self.board_pixel_size, self.padding, self.cell_size, p1.name)
        draw_legend(self.canvas, self.padding, self.padding + self.board_pixel_size + 40, 20)
        
        if self.auto_play:
            self.root.update()
            if self.delay > 0:
                time.sleep(self.delay)
            return

        self.advance = False
        while not self.advance and not self.trigger_enter and self.running and not self.auto_play:
            self.root.update()
            self.root.update_idletasks()
            time.sleep(0.01)
            
        if self.trigger_enter:
            self.fast_forward = True
            self.trigger_enter = False

    def show_round_result(self, p1, p2, iteration, winner_name):
        if not self.running: return

        self.canvas.delete("all")
        
        # Header
        self.canvas.create_text(self.padding, 20, text=f"Iteration: {iteration} - Finished", font=("Arial", 16, "bold"), anchor="w")
        
        # Winner
        window_width = int(self.canvas['width'])
        self.canvas.create_text(window_width / 2, 30, text=f"WINNER: {winner_name}", font=("Arial", 20, "bold"), fill="green")

        draw_board(self.canvas, p1.board, self.padding, self.padding, self.cell_size, p2.name)
        draw_board(self.canvas, p2.board, self.padding * 2 + self.board_pixel_size, self.padding, self.cell_size, p1.name)
        draw_legend(self.canvas, self.padding, self.padding + self.board_pixel_size + 40, 20)
        
        if self.auto_play:
            self.root.update()
            if self.delay > 0:
                time.sleep(self.delay)
        else:
            self.canvas.create_text(window_width / 2, int(self.canvas['height']) - 30, text="Press ENTER to continue", font=("Arial", 14), fill="blue")

        self.trigger_enter = False
        while not self.trigger_enter and self.running and not self.auto_play:
            self.root.update()
            self.root.update_idletasks()
            time.sleep(0.01)
            
        self.fast_forward = False
        self.trigger_enter = False

    def close(self):
        self.running = False
        self.root.destroy()

def show_game_state(p1, p2, winner_name=None):
    root = tk.Tk()
    root.title("Battleship Final Game State")

    cell_size = 30
    padding = 70
    board_pixel_size = 10 * cell_size
    
    window_width = padding * 3 + board_pixel_size * 2
    window_height = padding * 2 + board_pixel_size + 80

    canvas = tk.Canvas(root, width=window_width, height=window_height, bg="#f0f0f0")
    canvas.pack()

    if winner_name:
        canvas.create_text(window_width / 2, 30, text=f"WINNER: {winner_name}", font=("Arial", 20, "bold"), fill="green")

    draw_board(canvas, p1.board, padding, padding, cell_size, p1.name)
    draw_board(canvas, p2.board, padding * 2 + board_pixel_size, padding, cell_size, p2.name)

    draw_legend(canvas, padding, padding + board_pixel_size + 40, 20)

    print("Close the popup window to finish the script.")
    root.mainloop()

def get_player_selection(player_classes, descriptions):
    root = tk.Tk()
    root.title("Battleship - Select Players")
    
    selected_p1 = tk.StringVar(value=player_classes[0].__name__)
    selected_p2 = tk.StringVar(value=player_classes[1].__name__ if len(player_classes) > 1 else player_classes[0].__name__)
    
    selection = {"p1": None, "p2": None}

    def start():
        selection["p1"] = selected_p1.get()
        selection["p2"] = selected_p2.get()
        root.destroy()
        
    def on_close():
        sys.exit(0)

    root.protocol("WM_DELETE_WINDOW", on_close)

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack()

    tk.Label(frame, text="Player 1 Strategy", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w", padx=10)
    tk.Label(frame, text="Player 2 Strategy", font=("Arial", 12, "bold")).grid(row=0, column=1, sticky="w", padx=10)

    for i, cls in enumerate(player_classes):
        name = cls.__name__
        desc = descriptions.get(cls, "")
        
        for col, var in [(0, selected_p1), (1, selected_p2)]:
            p_frame = tk.Frame(frame)
            p_frame.grid(row=i+1, column=col, sticky="w", pady=5, padx=10)
            tk.Radiobutton(p_frame, text=name, variable=var, value=name, font=("Arial", 10, "bold")).pack(anchor="w")
            tk.Label(p_frame, text=desc, font=("Arial", 8), fg="#555555", wraplength=250, justify="left").pack(anchor="w", padx=20)

    tk.Button(frame, text="Start Simulation", command=start, font=("Arial", 12), bg="#e1e1e1", padx=20, pady=5).grid(row=len(player_classes)+1, column=0, columnspan=2, pady=20)

    root.mainloop()
    
    cls_map = {cls.__name__: cls for cls in player_classes}
    return cls_map[selection["p1"]], cls_map[selection["p2"]]