import tkinter as tk
from tkinter import messagebox
import random

WIDTH = 600
HEIGHT = 400
PADDLE_W = 15
PADDLE_H = 80
BALL_SIZE = 12
WIN_SCORE = 5


class PongGame:
    def __init__(self, root, back_callback=None):
        self.root = root
        self.back_callback = back_callback
        self.root.title("Pong")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#0a0a2e", highlightthickness=0)
        self.canvas.pack()

        self.top_frame = tk.Frame(root, bg="#0a0a2e")
        self.top_frame.pack(fill="x")
        self.score_label = tk.Label(self.top_frame, text="Player: 0  |  CPU: 0",
                                    font=("Helvetica", 14, "bold"), bg="#0a0a2e", fg="#eaeaea")
        self.score_label.pack(side="left", padx=10)
        tk.Button(self.top_frame, text="Restart", command=self.restart,
                  font=("Helvetica", 11), bg="#eaeaea", fg="black").pack(side="right", padx=10)
        tk.Button(self.top_frame, text="Menu", command=self.go_back,
                  font=("Helvetica", 11), bg="#eaeaea", fg="black").pack(side="right", padx=5)

        self.player_score = 0
        self.cpu_score = 0
        self.running = True

        self.player_paddle = self.canvas.create_rectangle(
            20, HEIGHT // 2 - PADDLE_H // 2, 20 + PADDLE_W, HEIGHT // 2 + PADDLE_H // 2, fill="#eaeaea"
        )
        self.cpu_paddle = self.canvas.create_rectangle(
            WIDTH - 35, HEIGHT // 2 - PADDLE_H // 2, WIDTH - 35 + PADDLE_W, HEIGHT // 2 + PADDLE_H // 2, fill="#e94560"
        )
        self.ball = self.canvas.create_oval(
            WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2,
            WIDTH // 2 + BALL_SIZE // 2, HEIGHT // 2 + BALL_SIZE // 2, fill="#f65e3b"
        )

        self.ball_dx = 4 * random.choice([-1, 1])
        self.ball_dy = 4 * random.choice([-1, 1])

        self.bind_keys()
        self.game_loop()

    def bind_keys(self):
        self.root.bind("<Up>", lambda e: self.move_player(-20))
        self.root.bind("<Down>", lambda e: self.move_player(20))
        self.root.bind("w", lambda e: self.move_player(-20))
        self.root.bind("s", lambda e: self.move_player(20))

    def move_player(self, dy):
        if not self.running:
            return
        pos = self.canvas.coords(self.player_paddle)
        new_y = pos[1] + dy
        if 0 <= new_y <= HEIGHT - PADDLE_H:
            self.canvas.move(self.player_paddle, 0, dy)

    def move_cpu(self):
        ball_pos = self.canvas.coords(self.ball)
        ball_y = (ball_pos[1] + ball_pos[3]) / 2
        cpu_pos = self.canvas.coords(self.cpu_paddle)
        cpu_y = (cpu_pos[1] + cpu_pos[3]) / 2

        speed = 3
        if ball_y < cpu_y - 10:
            self.canvas.move(self.cpu_paddle, 0, -speed)
        elif ball_y > cpu_y + 10:
            self.canvas.move(self.cpu_paddle, 0, speed)

        cpu_pos = self.canvas.coords(self.cpu_paddle)
        if cpu_pos[1] < 0:
            self.canvas.coords(self.cpu_paddle, cpu_pos[0], 0, cpu_pos[2], PADDLE_H)
        elif cpu_pos[3] > HEIGHT:
            self.canvas.coords(self.cpu_paddle, cpu_pos[0], HEIGHT - PADDLE_H, cpu_pos[2], HEIGHT)

    def game_loop(self):
        if not self.running:
            return

        self.move_cpu()
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        ball_pos = self.canvas.coords(self.ball)

        if ball_pos[1] <= 0 or ball_pos[3] >= HEIGHT:
            self.ball_dy = -self.ball_dy

        player_pos = self.canvas.coords(self.player_paddle)
        cpu_pos = self.canvas.coords(self.cpu_paddle)

        if (ball_pos[0] <= player_pos[2] and player_pos[1] <= ball_pos[3] <= player_pos[3]
                and self.ball_dx < 0):
            self.ball_dx = abs(self.ball_dx) + 0.5
            offset = ((ball_pos[1] + ball_pos[3]) / 2 - (player_pos[1] + player_pos[3]) / 2) / PADDLE_H * 6
            self.ball_dy = offset

        if (ball_pos[2] >= cpu_pos[0] and cpu_pos[1] <= ball_pos[3] <= cpu_pos[3]
                and self.ball_dx > 0):
            self.ball_dx = -abs(self.ball_dx) - 0.5
            offset = ((ball_pos[1] + ball_pos[3]) / 2 - (cpu_pos[1] + cpu_pos[3]) / 2) / PADDLE_H * 6
            self.ball_dy = offset

        if ball_pos[0] < 0:
            self.cpu_score += 1
            self.reset_ball()
        elif ball_pos[2] > WIDTH:
            self.player_score += 1
            self.reset_ball()

        self.score_label.config(text=f"Player: {self.player_score}  |  CPU: {self.cpu_score}")

        if self.player_score >= WIN_SCORE:
            self.running = False
            messagebox.showinfo("You Win!", "Congratulations!")
            return
        if self.cpu_score >= WIN_SCORE:
            self.running = False
            messagebox.showinfo("CPU Wins!", "Better luck next time!")
            return

        self.root.after(16, self.game_loop)

    def reset_ball(self):
        self.canvas.coords(self.ball, WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2,
                           WIDTH // 2 + BALL_SIZE // 2, HEIGHT // 2 + BALL_SIZE // 2)
        self.ball_dx = 4 * random.choice([-1, 1])
        self.ball_dy = 4 * random.choice([-1, 1])

    def restart(self):
        self.player_score = 0
        self.cpu_score = 0
        self.canvas.coords(self.player_paddle, 20, HEIGHT // 2 - PADDLE_H // 2, 20 + PADDLE_W, HEIGHT // 2 + PADDLE_H // 2)
        self.canvas.coords(self.cpu_paddle, WIDTH - 35, HEIGHT // 2 - PADDLE_H // 2, WIDTH - 35 + PADDLE_W, HEIGHT // 2 + PADDLE_H // 2)
        self.reset_ball()
        self.running = True
        self.game_loop()

    def go_back(self):
        self.running = False
        if self.back_callback:
            self.back_callback()


def check_paddle_collision(ball, paddle, ball_dx):
    b = ball
    p = paddle
    if b[0] <= p[2] and b[2] >= p[0] and b[1] <= p[3] and b[3] >= p[1]:
        return True
    return False


def bounce_angle(ball_y, paddle_y, paddle_height):
    relative = (ball_y - (paddle_y + paddle_height / 2)) / (paddle_height / 2)
    return relative * 6


def reset_ball_position(width, height, ball_size):
    return (width // 2 - ball_size // 2, height // 2 - ball_size // 2,
            width // 2 + ball_size // 2, height // 2 + ball_size // 2)


def check_score_limit(player_score, cpu_score, limit):
    if player_score >= limit:
        return "player"
    elif cpu_score >= limit:
        return "cpu"
    return None
