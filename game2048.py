import tkinter as tk
from tkinter import messagebox
import random

GRID_SIZE = 4
TILE_SIZE = 100
PADDING = 10
FONT_SIZE = 36
BOARD_SIZE = GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * PADDING

COLORS = {
    0: "#cdc1b4",
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e",
}


class Board:
    def __init__(self):
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.spawn_tile()
        self.spawn_tile()

    def spawn_tile(self):
        empty = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.grid[r][c] == 0]
        if empty:
            r, c = random.choice(empty)
            self.grid[r][c] = 4 if random.random() < 0.1 else 2

    def compress(self, row):
        tiles = [x for x in row if x != 0]
        tiles += [0] * (GRID_SIZE - len(tiles))
        return tiles

    def merge(self, row):
        for i in range(GRID_SIZE - 1):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                self.score += row[i]
                row[i + 1] = 0
        return row

    def move_left(self):
        moved = False
        for r in range(GRID_SIZE):
            original = self.grid[r][:]
            compressed = self.compress(self.grid[r])
            merged = self.merge(compressed)
            final = self.compress(merged)
            self.grid[r] = final
            if final != original:
                moved = True
        return moved

    def move_right(self):
        moved = False
        for r in range(GRID_SIZE):
            original = self.grid[r][:]
            reversed_row = self.grid[r][::-1]
            compressed = self.compress(reversed_row)
            merged = self.merge(compressed)
            final = self.compress(merged)[::-1]
            self.grid[r] = final
            if final != original:
                moved = True
        return moved

    def move_up(self):
        moved = False
        for c in range(GRID_SIZE):
            original = [self.grid[r][c] for r in range(GRID_SIZE)]
            column = [self.grid[r][c] for r in range(GRID_SIZE)]
            compressed = self.compress(column)
            merged = self.merge(compressed)
            final = self.compress(merged)
            for r in range(GRID_SIZE):
                self.grid[r][c] = final[r]
            if final != original:
                moved = True
        return moved

    def move_down(self):
        moved = False
        for c in range(GRID_SIZE):
            original = [self.grid[r][c] for r in range(GRID_SIZE)]
            column = [self.grid[r][c] for r in range(GRID_SIZE)][::-1]
            compressed = self.compress(column)
            merged = self.merge(compressed)
            final = self.compress(merged)[::-1]
            for r in range(GRID_SIZE):
                self.grid[r][c] = final[r]
            if final != original:
                moved = True
        return moved

    def has_moves(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c] == 0:
                    return True
                if c < GRID_SIZE - 1 and self.grid[r][c] == self.grid[r][c + 1]:
                    return True
                if r < GRID_SIZE - 1 and self.grid[r][c] == self.grid[r + 1][c]:
                    return True
        return False

    def has_won(self):
        return any(self.grid[r][c] >= 2048 for r in range(GRID_SIZE) for c in range(GRID_SIZE))

    def reset(self):
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.spawn_tile()
        self.spawn_tile()


class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048")
        self.root.resizable(False, False)

        self.board = Board()
        self.canvas = tk.Canvas(root, width=BOARD_SIZE, height=BOARD_SIZE + 60, bg="#faf8ef")
        self.canvas.pack()

        self.draw_board()
        self.bind_keys()

    def draw_board(self):
        self.canvas.delete("all")
        self.canvas.create_text(
            BOARD_SIZE // 2, 30, text=f"Score: {self.board.score}",
            font=("Helvetica", 20, "bold"), fill="#776e65"
        )

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x = c * (TILE_SIZE + PADDING) + PADDING
                y = r * (TILE_SIZE + PADDING) + PADDING + 50
                value = self.board.grid[r][c]
                color = COLORS.get(value, "#3c3a32")
                text_color = "#f9f6f2" if value >= 8 else "#776e65"

                self.canvas.create_rectangle(x, y, x + TILE_SIZE, y + TILE_SIZE, fill=color, outline="")
                if value != 0:
                    self.canvas.create_text(
                        x + TILE_SIZE // 2, y + TILE_SIZE // 2,
                        text=str(value), font=("Helvetica", FONT_SIZE, "bold"), fill=text_color
                    )

    def bind_keys(self):
        self.root.bind("<Left>", lambda e: self.move("left"))
        self.root.bind("<Right>", lambda e: self.move("right"))
        self.root.bind("<Up>", lambda e: self.move("up"))
        self.root.bind("<Down>", lambda e: self.move("down"))
        self.root.bind("r", lambda e: self.restart())

    def move(self, direction):
        moves = {
            "left": self.board.move_left,
            "right": self.board.move_right,
            "up": self.board.move_up,
            "down": self.board.move_down,
        }

        moved = moves[direction]()
        if moved:
            self.board.spawn_tile()
            self.draw_board()

            if self.board.has_won():
                messagebox.showinfo("You Win!", f"You reached 2048! Score: {self.board.score}")
            elif not self.board.has_moves():
                messagebox.showinfo("Game Over", f"No moves left. Score: {self.board.score}")

    def restart(self):
        self.board.reset()
        self.draw_board()


def compress_row(row):
    return [x for x in row if x != 0] + [0] * (len(row) - len([x for x in row if x != 0]))


def merge_row(row):
    for i in range(len(row) - 1):
        if row[i] != 0 and row[i] == row[i + 1]:
            row[i] *= 2
            row[i + 1] = 0
    return row


def is_grid_full(grid):
    return all(grid[r][c] != 0 for r in range(len(grid)) for c in range(len(grid[0])))


def get_empty_cells(grid):
    return [(r, c) for r in range(len(grid)) for c in range(len(grid[0])) if grid[r][c] == 0]


def max_tile(grid):
    return max(grid[r][c] for r in range(len(grid)) for c in range(len(grid[0])))


def can_merge(grid):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            val = grid[r][c]
            if c + 1 < len(grid[0]) and val == grid[r][c + 1]:
                return True
            if r + 1 < len(grid) and val == grid[r + 1][c]:
                return True
    return False


if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
