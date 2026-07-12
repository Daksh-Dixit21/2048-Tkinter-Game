# Python Game Hub

A collection of 5 classic games built with Python tkinter. No external dependencies required.

## Games Included

| Game | Controls | Description |
|------|----------|-------------|
| **2048** | Arrow keys | Slide tiles, merge numbers, reach 2048 |
| **Snake** | Arrow keys / WASD | Eat food, grow longer, don't crash |
| **Tic-Tac-Toe** | Mouse click | Play vs AI opponent |
| **Pong** | Up/Down arrows | First to 5 wins against CPU |
| **Breakout** | Left/Right arrows | Smash all bricks to win |

## How to Run

```bash
python main.py
```

## Project Structure

- `main.py` - Game hub with menu and game launcher
- `game2048.py` - 2048 sliding tile puzzle
- `snake.py` - Classic snake game
- `tictactoe.py` - Tic-tac-toe with AI
- `pong.py` - Single player pong
- `breakout.py` - Brick breaker game

<!-- AUTODOCS:OVERVIEW:START -->
**Primary language:** Python

**Total files:** 8

**Entry point:** `main.py`
<!-- AUTODOCS:OVERVIEW:END -->

<!-- AUTODOCS:API:START -->
_No API routes detected._
<!-- AUTODOCS:API:END -->

<!-- AUTODOCS:ARCHITECTURE:START -->
```mermaid
graph TD
__init__ --> spawn_tile
__init__ --> spawn_tile
move_left --> compress
move_left --> merge
move_left --> compress
move_right --> compress
move_right --> merge
move_right --> compress
move_up --> compress
move_up --> merge
move_up --> compress
move_down --> compress
move_down --> merge
move_down --> compress
reset --> spawn_tile
reset --> spawn_tile
__init__ --> draw_board
__init__ --> move
__init__ --> move
__init__ --> move
__init__ --> move
move --> spawn_tile
move --> draw_board
move --> has_won
move --> has_moves
restart --> reset
restart --> draw_board
__init__ --> spawn_food
__init__ --> bind_keys
__init__ --> game_loop
bind_keys --> set_direction
bind_keys --> set_direction
bind_keys --> set_direction
bind_keys --> set_direction
bind_keys --> set_direction
bind_keys --> set_direction
bind_keys --> set_direction
bind_keys --> set_direction
move_snake --> spawn_food
game_loop --> move_snake
game_loop --> draw
restart --> spawn_food
restart --> draw
restart --> game_loop
__init__ --> create_bricks
__init__ --> bind_keys
__init__ --> game_loop
bind_keys --> move_paddle
bind_keys --> move_paddle
bind_keys --> move_paddle
bind_keys --> move_paddle
game_loop --> reset_ball
restart --> create_bricks
restart --> game_loop
__init__ --> draw_menu
draw_menu --> draw_button
draw_button --> launch_game
draw_button --> hover
draw_button --> hover
back_to_menu --> draw_menu
__init__ --> bind_keys
__init__ --> game_loop
bind_keys --> move_player
bind_keys --> move_player
bind_keys --> move_player
bind_keys --> move_player
game_loop --> move_cpu
game_loop --> reset_ball
game_loop --> reset_ball
restart --> reset_ball
restart --> game_loop
minimax --> check_winner
minimax --> check_winner
minimax --> is_board_full
minimax --> get_empty_cells
minimax --> get_empty_cells
minimax --> minimax
minimax --> minimax
find_best_move --> get_empty_cells
find_best_move --> minimax
__init__ --> draw_board
click --> draw_board
click --> check_winner
ai_move --> find_best_move
ai_move --> draw_board
ai_move --> check_winner
find_best_move --> check_winner
find_best_move --> check_winner
restart --> draw_board
```
<!-- AUTODOCS:ARCHITECTURE:END -->
