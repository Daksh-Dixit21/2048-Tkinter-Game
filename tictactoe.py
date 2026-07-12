import tkinter as tk
from tkinter import messagebox
import random

BOARD_SIZE = 3
CELL_SIZE = 150
CANVAS_SIZE = BOARD_SIZE * CELL_SIZE


class TicTacToe:
    def __init__(self, root, back_callback=None):
        self.root = root
        self.back_callback = back_callback
        self.root.title("Tic-Tac-Toe")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE, bg="#1a1a2e")
        self.canvas.pack()

        self.top_frame = tk.Frame(root, bg="#1a1a2e")
        self.top_frame.pack(fill="x")
        self.status_label = tk.Label(self.top_frame, text="Your turn (X)", font=("Helvetica", 16, "bold"),
                                     bg="#1a1a2e", fg="#3282b8")
        self.status_label.pack(side="left", padx=10)
        tk.Button(self.top_frame, text="Restart", command=self.restart,
                  font=("Helvetica", 11), bg="#3282b8", fg="white").pack(side="right", padx=10)
        tk.Button(self.top_frame, text="Menu", command=self.go_back,
                  font=("Helvetica", 11), bg="#3282b8", fg="white").pack(side="right", padx=5)

        self.board = [""] * 9
        self.player = "X"
        self.ai = "O"
        self.game_over = False

        self.draw_board()
        self.canvas.bind("<Button-1>", self.click)

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(1, BOARD_SIZE):
            self.canvas.create_line(i * CELL_SIZE, 0, i * CELL_SIZE, CANVAS_SIZE, fill="#3a3a5c", width=2)
            self.canvas.create_line(0, i * CELL_SIZE, CANVAS_SIZE, i * CELL_SIZE, fill="#3a3a5c", width=2)

        for i, mark in enumerate(self.board):
            if mark:
                row, col = divmod(i, 3)
                x = col * CELL_SIZE + CELL_SIZE // 2
                y = row * CELL_SIZE + CELL_SIZE // 2
                color = "#3282b8" if mark == "X" else "#e94560"
                self.canvas.create_text(x, y, text=mark, font=("Helvetica", 60, "bold"), fill=color)

    def click(self, event):
        if self.game_over:
            return
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        idx = row * 3 + col

        if self.board[idx] == "":
            self.board[idx] = self.player
            self.draw_board()

            if self.check_winner(self.player):
                self.game_over = True
                self.status_label.config(text="You win!")
                messagebox.showinfo("Game Over", "You win!")
                return
            if all(cell != "" for cell in self.board):
                self.game_over = True
                self.status_label.config(text="It's a tie!")
                messagebox.showinfo("Game Over", "It's a tie!")
                return

            self.status_label.config(text="AI thinking...")
            self.root.after(400, self.ai_move)

    def ai_move(self):
        if self.game_over:
            return
        idx = self.find_best_move()
        self.board[idx] = self.ai
        self.draw_board()

        if self.check_winner(self.ai):
            self.game_over = True
            self.status_label.config(text="AI wins!")
            messagebox.showinfo("Game Over", "AI wins!")
            return
        if all(cell != "" for cell in self.board):
            self.game_over = True
            self.status_label.config(text="It's a tie!")
            messagebox.showinfo("Game Over", "It's a tie!")
            return

        self.status_label.config(text="Your turn (X)")

    def find_best_move(self):
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = self.ai
                if self.check_winner(self.ai):
                    self.board[i] = ""
                    return i
                self.board[i] = ""

        for i in range(9):
            if self.board[i] == "":
                self.board[i] = self.player
                if self.check_winner(self.player):
                    self.board[i] = ""
                    return i
                self.board[i] = ""

        if self.board[4] == "":
            return 4

        corners = [0, 2, 6, 8]
        empty_corners = [i for i in corners if self.board[i] == ""]
        if empty_corners:
            return random.choice(empty_corners)

        empty = [i for i in range(9) if self.board[i] == ""]
        return random.choice(empty)

    def check_winner(self, mark):
        wins = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        return any(all(self.board[i] == mark for i in combo) for combo in wins)

    def restart(self):
        self.board = [""] * 9
        self.game_over = False
        self.status_label.config(text="Your turn (X)")
        self.draw_board()

    def go_back(self):
        self.game_over = True
        if self.back_callback:
            self.back_callback()


def check_winner(board, mark):
    wins = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]]
    return any(all(board[i] == mark for i in combo) for combo in wins)


def is_board_full(board):
    return all(cell != "" for cell in board)


def get_empty_cells(board):
    return [i for i in range(9) if board[i] == ""]


def minimax(board, depth, is_maximizing):
    if check_winner(board, "O"):
        return 10 - depth
    if check_winner(board, "X"):
        return depth - 10
    if is_board_full(board):
        return 0

    if is_maximizing:
        best = -100
        for i in get_empty_cells(board):
            board[i] = "O"
            best = max(best, minimax(board, depth + 1, False))
            board[i] = ""
        return best
    else:
        best = 100
        for i in get_empty_cells(board):
            board[i] = "X"
            best = min(best, minimax(board, depth + 1, True))
            board[i] = ""
        return best


def find_best_move(board):
    best_score = -100
    best_move = -1
    for i in get_empty_cells(board):
        board[i] = "O"
        score = minimax(board, 0, False)
        board[i] = ""
        if score > best_score:
            best_score = score
            best_move = i
    return best_move
