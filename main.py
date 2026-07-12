import tkinter as tk
from tkinter import font as tkfont

class GameHub:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Game Hub")
        self.root.resizable(False, False)

        self.WIDTH = 500
        self.HEIGHT = 600
        self.bg_color = "#1a1a2e"
        self.accent = "#e94560"
        self.text_color = "#eaeaea"

        self.canvas = tk.Canvas(root, width=self.WIDTH, height=self.HEIGHT, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack()

        self.draw_menu()

    def draw_menu(self):
        self.canvas.delete("all")

        self.canvas.create_text(
            self.WIDTH // 2, 60,
            text="PYTHON GAME HUB",
            font=("Helvetica", 32, "bold"), fill=self.accent
        )
        self.canvas.create_text(
            self.WIDTH // 2, 100,
            text="Pick a game to play",
            font=("Helvetica", 14), fill="#888"
        )

        games = [
            ("2048", "Slide tiles, merge numbers, reach 2048", "#f65e3b"),
            ("Snake", "Eat food, grow longer, don't crash", "#4ecca3"),
            ("Tic-Tac-Toe", "Classic X and O, play vs AI", "#3282b8"),
            ("Pong", "First to 5 wins, arrow keys only", "#eaeaea"),
            ("Breakout", "Smash all bricks to win", "#f9ed69"),
        ]

        for i, (name, desc, color) in enumerate(games):
            y = 160 + i * 85
            self.draw_button(100, y, 400, y + 65, name, desc, color, name)

    def draw_button(self, x1, y1, x2, y2, title, subtitle, color, game_name):
        tag = f"btn_{game_name}"
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#16213e", outline=color, width=2, tags=tag)
        self.canvas.create_text(
            (x1 + x2) // 2, y1 + 22,
            text=title, font=("Helvetica", 18, "bold"), fill=color, tags=tag
        )
        self.canvas.create_text(
            (x1 + x2) // 2, y1 + 46,
            text=subtitle, font=("Helvetica", 10), fill="#888", tags=tag
        )
        self.canvas.tag_bind(tag, "<Button-1>", lambda e, g=game_name: self.launch_game(g))
        self.canvas.tag_bind(tag, "<Enter>", lambda e, t=tag: self.hover(t, True))
        self.canvas.tag_bind(tag, "<Leave>", lambda e, t=tag: self.hover(t, False))

    def hover(self, tag, enter):
        items = self.canvas.find_withtag(tag)
        for item in items:
            if self.canvas.type(item) == "rectangle":
                self.canvas.itemconfig(item, fill="#0f3460" if enter else "#16213e")

    def launch_game(self, game_name):
        for widget in self.root.winfo_children():
            if widget != self.canvas:
                widget.destroy()

        self.canvas.pack_forget()

        if game_name == "2048":
            from game2048 import Game2048
            Game2048(self.root, self.back_to_menu)
        elif game_name == "Snake":
            from snake import SnakeGame
            SnakeGame(self.root, self.back_to_menu)
        elif game_name == "Tic-Tac-Toe":
            from tictactoe import TicTacToe
            TicTacToe(self.root, self.back_to_menu)
        elif game_name == "Pong":
            from pong import PongGame
            PongGame(self.root, self.back_to_menu)
        elif game_name == "Breakout":
            from breakout import BreakoutGame
            BreakoutGame(self.root, self.back_to_menu)

    def back_to_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.canvas = tk.Canvas(self.root, width=self.WIDTH, height=self.HEIGHT, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack()
        self.draw_menu()


if __name__ == "__main__":
    root = tk.Tk()
    app = GameHub(root)
    root.mainloop()
