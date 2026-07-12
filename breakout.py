import tkinter as tk
from tkinter import messagebox
import random

WIDTH = 600
HEIGHT = 450
PADDLE_W = 100
PADDLE_H = 15
BALL_SIZE = 10
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_W = 55
BRICK_H = 20
BRICK_PAD = 5
BRICK_OFFSET_X = 15
BRICK_OFFSET_Y = 40

BRICK_COLORS = ["#e94560", "#f65e3b", "#f9ed69", "#4ecca3", "#3282b8"]


class BreakoutGame:
    def __init__(self, root, back_callback=None):
        self.root = root
        self.back_callback = back_callback
        self.root.title("Breakout")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#0f0f23", highlightthickness=0)
        self.canvas.pack()

        self.top_frame = tk.Frame(root, bg="#0f0f23")
        self.top_frame.pack(fill="x")
        self.score_label = tk.Label(self.top_frame, text="Score: 0  |  Lives: 3",
                                    font=("Helvetica", 14, "bold"), bg="#0f0f23", fg="#f9ed69")
        self.score_label.pack(side="left", padx=10)
        tk.Button(self.top_frame, text="Restart", command=self.restart,
                  font=("Helvetica", 11), bg="#f9ed69", fg="black").pack(side="right", padx=10)
        tk.Button(self.top_frame, text="Menu", command=self.go_back,
                  font=("Helvetica", 11), bg="#f9ed69", fg="black").pack(side="right", padx=5)

        self.score = 0
        self.lives = 3
        self.running = True
        self.ball_dx = 4
        self.ball_dy = -4

        self.paddle = self.canvas.create_rectangle(
            WIDTH // 2 - PADDLE_W // 2, HEIGHT - 30,
            WIDTH // 2 + PADDLE_W // 2, HEIGHT - 30 + PADDLE_H, fill="#eaeaea"
        )
        self.ball = self.canvas.create_oval(
            WIDTH // 2 - BALL_SIZE // 2, HEIGHT - 45,
            WIDTH // 2 + BALL_SIZE // 2, HEIGHT - 45 + BALL_SIZE, fill="#f9ed69"
        )

        self.bricks = []
        self.create_bricks()

        self.bind_keys()
        self.game_loop()

    def create_bricks(self):
        self.bricks = []
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = BRICK_OFFSET_X + col * (BRICK_W + BRICK_PAD)
                y = BRICK_OFFSET_Y + row * (BRICK_H + BRICK_PAD)
                color = BRICK_COLORS[row % len(BRICK_COLORS)]
                brick = self.canvas.create_rectangle(x, y, x + BRICK_W, y + BRICK_H,
                                                     fill=color, outline="#0f0f23", tags="brick")
                self.bricks.append(brick)

    def bind_keys(self):
        self.root.bind("<Left>", lambda e: self.move_paddle(-25))
        self.root.bind("<Right>", lambda e: self.move_paddle(25))
        self.root.bind("a", lambda e: self.move_paddle(-25))
        self.root.bind("d", lambda e: self.move_paddle(25))

    def move_paddle(self, dx):
        if not self.running:
            return
        pos = self.canvas.coords(self.paddle)
        new_x = pos[0] + dx
        if 0 <= new_x <= WIDTH - PADDLE_W:
            self.canvas.move(self.paddle, dx, 0)

    def game_loop(self):
        if not self.running:
            return

        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        ball_pos = self.canvas.coords(self.ball)

        if ball_pos[1] <= 0:
            self.ball_dy = abs(self.ball_dy)
        if ball_pos[0] <= 0 or ball_pos[2] >= WIDTH:
            self.ball_dx = -self.ball_dx

        paddle_pos = self.canvas.coords(self.paddle)
        if (ball_pos[3] >= paddle_pos[1] and ball_pos[0] <= paddle_pos[2]
                and ball_pos[2] >= paddle_pos[0] and self.ball_dy > 0):
            self.ball_dy = -abs(self.ball_dy)
            offset = ((ball_pos[0] + ball_pos[2]) / 2 - (paddle_pos[0] + paddle_pos[2]) / 2) / PADDLE_W * 8
            self.ball_dx = max(-6, min(6, self.ball_dx + offset))

        for brick in self.bricks[:]:
            brick_pos = self.canvas.coords(brick)
            if (ball_pos[2] >= brick_pos[0] and ball_pos[0] <= brick_pos[2]
                    and ball_pos[3] >= brick_pos[1] and ball_pos[1] <= brick_pos[3]):
                self.canvas.delete(brick)
                self.bricks.remove(brick)
                self.ball_dy = -self.ball_dy
                self.score += 10
                break

        if ball_pos[3] >= HEIGHT:
            self.lives -= 1
            if self.lives <= 0:
                self.running = False
                messagebox.showinfo("Game Over", f"Score: {self.score}")
                return
            self.reset_ball()

        if not self.bricks:
            self.running = False
            messagebox.showinfo("You Win!", f"Score: {self.score}")
            return

        self.score_label.config(text=f"Score: {self.score}  |  Lives: {self.lives}")
        self.root.after(16, self.game_loop)

    def reset_ball(self):
        self.canvas.coords(self.ball, WIDTH // 2 - BALL_SIZE // 2, HEIGHT - 45,
                           WIDTH // 2 + BALL_SIZE // 2, HEIGHT - 45 + BALL_SIZE)
        self.ball_dx = 4 * random.choice([-1, 1])
        self.ball_dy = -4

    def restart(self):
        self.canvas.delete("all")
        self.score = 0
        self.lives = 3
        self.running = True
        self.ball_dx = 4
        self.ball_dy = -4

        self.paddle = self.canvas.create_rectangle(
            WIDTH // 2 - PADDLE_W // 2, HEIGHT - 30,
            WIDTH // 2 + PADDLE_W // 2, HEIGHT - 30 + PADDLE_H, fill="#eaeaea"
        )
        self.ball = self.canvas.create_oval(
            WIDTH // 2 - BALL_SIZE // 2, HEIGHT - 45,
            WIDTH // 2 + BALL_SIZE // 2, HEIGHT - 45 + BALL_SIZE, fill="#f9ed69"
        )
        self.create_bricks()
        self.game_loop()

    def go_back(self):
        self.running = False
        if self.back_callback:
            self.back_callback()


def check_ball_brick_collision(ball, brick):
    b = ball
    br = brick
    return b[2] >= br[0] and b[0] <= br[2] and b[3] >= br[1] and b[1] <= br[3]


def calculate_score(bricks_destroyed, base=10):
    return bricks_destroyed * base


def random_ball_direction():
    dx = 4 * random.choice([-1, 1])
    dy = -4
    return dx, dy


def create_bricks(rows, cols, width, offset_x, offset_y):
    bricks = []
    brick_w = (width - offset_x * 2) // cols - 5
    for row in range(rows):
        for col in range(cols):
            x = offset_x + col * (brick_w + 5)
            y = offset_y + row * 25
            bricks.append({"x": x, "y": y, "w": brick_w, "h": 20})
    return bricks
