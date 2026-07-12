import tkinter as tk
from tkinter import messagebox
import random

CELL = 20
COLS = 25
ROWS = 25
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL


class SnakeGame:
    def __init__(self, root, back_callback=None):
        self.root = root
        self.back_callback = back_callback
        self.root.title("Snake")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#0f0f23", highlightthickness=0)
        self.canvas.pack()

        self.top_frame = tk.Frame(root, bg="#0f0f23")
        self.top_frame.pack(fill="x")
        self.score_label = tk.Label(self.top_frame, text="Score: 0", font=("Helvetica", 14, "bold"),
                                    bg="#0f0f23", fg="#4ecca3")
        self.score_label.pack(side="left", padx=10)
        tk.Button(self.top_frame, text="Restart", command=self.restart,
                  font=("Helvetica", 11), bg="#4ecca3", fg="black").pack(side="right", padx=10)
        tk.Button(self.top_frame, text="Menu", command=self.go_back,
                  font=("Helvetica", 11), bg="#4ecca3", fg="black").pack(side="right", padx=5)

        self.direction = "Right"
        self.next_direction = "Right"
        self.running = True
        self.score = 0
        self.snake = [(12, 12), (11, 12), (10, 12)]
        self.food = None
        self.spawn_food()
        self.bind_keys()
        self.game_loop()

    def spawn_food(self):
        while True:
            x = random.randint(0, COLS - 1)
            y = random.randint(0, ROWS - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def bind_keys(self):
        self.root.bind("<Left>", lambda e: self.set_direction("Left"))
        self.root.bind("<Right>", lambda e: self.set_direction("Right"))
        self.root.bind("<Up>", lambda e: self.set_direction("Up"))
        self.root.bind("<Down>", lambda e: self.set_direction("Down"))
        self.root.bind("w", lambda e: self.set_direction("Up"))
        self.root.bind("a", lambda e: self.set_direction("Left"))
        self.root.bind("s", lambda e: self.set_direction("Down"))
        self.root.bind("d", lambda e: self.set_direction("Right"))

    def set_direction(self, new_dir):
        opposites = {"Left": "Right", "Right": "Left", "Up": "Down", "Down": "Up"}
        if new_dir != opposites.get(self.direction):
            self.next_direction = new_dir

    def move_snake(self):
        self.direction = self.next_direction
        head_x, head_y = self.snake[0]

        if self.direction == "Right":
            head_x += 1
        elif self.direction == "Left":
            head_x -= 1
        elif self.direction == "Up":
            head_y -= 1
        elif self.direction == "Down":
            head_y += 1

        new_head = (head_x, head_y)

        if (head_x < 0 or head_x >= COLS or head_y < 0 or head_y >= ROWS
                or new_head in self.snake):
            self.running = False
            messagebox.showinfo("Game Over", f"Score: {self.score}")
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 10
            self.spawn_food()
        else:
            self.snake.pop()

    def draw(self):
        self.canvas.delete("all")
        self.score_label.config(text=f"Score: {self.score}")

        for i, (x, y) in enumerate(self.snake):
            color = "#4ecca3" if i == 0 else "#3a8f73"
            self.canvas.create_rectangle(x * CELL, y * CELL, x * CELL + CELL, y * CELL + CELL,
                                         fill=color, outline="#0f0f23")

        fx, fy = self.food
        self.canvas.create_oval(fx * CELL + 2, fy * CELL + 2, fx * CELL + CELL - 2, fy * CELL + CELL - 2,
                                fill="#e94560", outline="")

    def game_loop(self):
        if not self.running:
            return
        self.move_snake()
        if self.running:
            self.draw()
            self.root.after(100, self.game_loop)

    def restart(self):
        self.direction = "Right"
        self.next_direction = "Right"
        self.running = True
        self.score = 0
        self.snake = [(12, 12), (11, 12), (10, 12)]
        self.spawn_food()
        self.draw()
        self.game_loop()

    def go_back(self):
        self.running = False
        if self.back_callback:
            self.back_callback()


def check_collision(head, body):
    return head in body


def is_out_of_bounds(pos, width, height):
    return pos[0] < 0 or pos[0] >= width or pos[1] < 0 or pos[1] >= height


def grow_snake(snake, direction):
    head = snake[0]
    if direction == "Right":
        return (head[0] + 1, head[1])
    elif direction == "Left":
        return (head[0] - 1, head[1])
    elif direction == "Up":
        return (head[0], head[1] - 1)
    elif direction == "Down":
        return (head[0], head[1] + 1)


def random_food_position(snake, cols, rows):
    while True:
        pos = (random.randint(0, cols - 1), random.randint(0, rows - 1))
        if pos not in snake:
            return pos


def calculate_score(food_eaten, base=10):
    return food_eaten * base
