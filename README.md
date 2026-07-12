# 2048 Game

A fully functional 2048 puzzle game built with Python tkinter. Slide tiles, merge matching numbers, and reach 2048!

## How to Play

```bash
python game2048.py
```

- **Arrow keys** to move tiles (Left, Right, Up, Down)
- **R** to restart
- Tiles with the same number merge when they collide
- Goal: create a tile with the value **2048**

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
