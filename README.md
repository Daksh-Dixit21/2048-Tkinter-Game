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

**Total files:** 3
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
__init__ --> bind_keys
bind_keys --> move
bind_keys --> move
bind_keys --> move
bind_keys --> move
bind_keys --> restart
move --> spawn_tile
move --> draw_board
move --> has_won
move --> has_moves
restart --> reset
restart --> draw_board
```
<!-- AUTODOCS:ARCHITECTURE:END -->
