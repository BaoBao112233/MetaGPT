Okay, let's create a text-based 2048 game in Python!

This script will:
1.  Represent the board as a 2D list.
2.  Handle adding new random tiles (2 or 4).
3.  Implement the core sliding and merging logic for all four directions (up, down, left, right).
4.  Check for win (reaching 2048) and lose (no more moves).
5.  Display the board in the console.

```python
import random
import copy
import os # For clearing the console

# --- Game Constants ---
GRID_SIZE = 4
TARGET_TILE = 2048

# --- Helper Functions ---

def clear_console():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def initialize_game():
    """Creates an empty 4x4 grid and adds two initial random tiles."""
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    score = 0
    add_random_tile(grid)
    add_random_tile(grid)
    return grid, score

def print_grid(grid, score):
    """Prints the current state of the 2048 grid."""
    clear_console()
    print("--- 2048 Game ---")
    print(f"Score: {score}\n")
    print("+" + "------+" * GRID_SIZE)
    for row in grid:
        row_str = "|"
        for cell in row:
            if cell == 0:
                row_str += "      |"
            else:
                row_str += f"{cell:^6}|" # Center align number in 6 spaces
        print(row_str)
        print("+" + "------+" * GRID_SIZE)
    print("\nUse W/A/S/D to move, Q to quit.")

def get_empty_cells(grid):
    """Returns a list of (row, col) tuples for all empty cells (value 0)."""
    empty_cells = []
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == 0:
                empty_cells.append((r, c))
    return empty_cells

def add_random_tile(grid):
    """Adds a new tile (2 or 4) to a random empty cell."""
    empty_cells = get_empty_cells(grid)
    if empty_cells:
        r, c = random.choice(empty_cells)
        grid[r][c] = 2 if random.random() < 0.9 else 4 # 90% chance for 2, 10% for 4

# --- Core Game Logic (Sliding and Merging) ---

def _slide_row(row):
    """Slides non-zero tiles to the beginning of a row, filling empty spaces with zeros."""
    new_row = [tile for tile in row if tile != 0]
    new_row.extend([0] * (GRID_SIZE - len(new_row)))
    return new_row

def _merge_row(row):
    """Merges adjacent identical tiles in a row and returns the new row and score added."""
    score_added = 0
    for i in range(GRID_SIZE - 1):
        if row[i] != 0 and row[i] == row[i+1]:
            row[i] *= 2
            score_added += row[i]
            row[i+1] = 0 # Mark the merged tile as empty
    return row, score_added

def move(grid, direction):
    """
    Applies a move (up, down, left, right) to the grid.
    Returns (new_grid, score_added, moved_occurred).
    """
    original_grid = copy.deepcopy(grid)
    new_grid = copy.deepcopy(grid)
    score_added = 0
    moved_occurred = False

    if direction == 'left':
        for r in range(GRID_SIZE):
            row = new_grid[r]
            slid_row = _slide_row(row)
            merged_row, s_add = _merge_row(slid_row)
            score_added += s_add
            final_row = _slide_row(merged_row) # Slide again after merge
            new_grid[r] = final_row

    elif direction == 'right':
        for r in range(GRID_SIZE):
            row = new_grid[r]
            row.reverse() # Reverse to treat as left slide
            slid_row = _slide_row(row)
            merged_row, s_add = _merge_row(slid_row)
            score_added += s_add
            final_row = _slide_row(merged_row)
            final_row.reverse() # Reverse back
            new_grid[r] = final_row

    elif direction == 'up':
        # Transpose grid to treat columns as rows
        transposed_grid = [list(col) for col in zip(*new_grid)]
        for c in range(GRID_SIZE):
            col = transposed_grid[c]
            slid_col = _slide_row(col)
            merged_col, s_add = _merge_row(slid_col)
            score_added += s_add
            final_col = _slide_row(merged_col)
            transposed_grid[c] = final_col
        # Transpose back
        new_grid = [list(row) for row in zip(*transposed_grid)]

    elif direction == 'down':
        # Transpose grid
        transposed_grid = [list(col) for col in zip(*new_grid)]
        for c in range(GRID_SIZE):
            col = transposed_grid[c]
            col.reverse() # Reverse to treat as up slide
            slid_col = _slide_row(col)
            merged_col, s_add = _merge_row(slid_col)
            score_added += s_add
            final_col = _slide_row(merged_col)
            final_col.reverse() # Reverse back
            transposed_grid[c] = final_col
        # Transpose back
        new_grid = [list(row) for row in zip(*transposed_grid)]

    if new_grid != original_grid:
        moved_occurred = True

    return new_grid, score_added, moved_occurred

# --- Game State Checks ---

def check_win(grid):
    """Checks if the 2048 tile has been reached."""
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == TARGET_TILE:
                return True
    return False

def check_lose(grid):
    """Checks if there are no more possible moves (grid full and no merges)."""
    if get_empty_cells(grid):
        return False # Still empty cells, so not lost

    # Check for possible merges horizontally
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE - 1):
            if grid[r][c] == grid[r][c+1]:
                return False # Merge possible

    # Check for possible merges vertically
    for c in range(GRID_SIZE):
        for r in range(GRID_SIZE - 1):
            if grid[r][c] == grid[r+1][c]:
                return False # Merge possible

    return True # No empty cells and no merges possible

# --- Main Game Loop ---

def main():
    grid, score = initialize_game()
    game_over = False
    game_won = False

    while not game_over and not game_won:
        print_grid(grid, score)

        # Get player input
        move_input = input("Your move (W/A/S/D) or Q to quit: ").lower()

        if move_input == 'q':
            game_over = True
            print("Quitting game. Thanks for playing!")
            break

        if move_input not in ['w', 'a', 's', 'd']:
            print("Invalid input. Please use W, A, S, D, or Q.")
            input("Press Enter to continue...") # Pause for user to read message
            continue

        # Apply the move
        new_grid, score_added, moved_occurred = move(grid, move_input)

        if moved_occurred:
            grid = new_grid
            score += score_added
            add_random_tile(grid) # Add new tile only if a move actually happened

            if check_win(grid):
                game_won = True
                print_grid(grid, score)
                print("\n--- CONGRATULATIONS! YOU REACHED 2048! YOU WIN! ---")
            elif check_lose(grid):
                game_over = True
                print_grid(grid, score)
                print("\n--- GAME OVER! No more moves possible. ---")
        else:
            print("No move occurred. Try a different direction.")
            input("Press Enter to continue...") # Pause for user to read message

    if game_over and not game_won:
        print(f"Final Score: {score}")
    elif game_won:
        print(f"Final Score: {score}")

if __name__ == "__main__":
    main()
```

### How to Play:

1.  **Save:** Save the code as a Python file (e.g., `2048_game.py`).
2.  **Run:** Open a terminal or command prompt, navigate to the directory where you saved the file, and run it using `python 2048_game.py`.
3.  **Controls:**
    *   `W`: Move tiles Up
    *   `A`: Move tiles Left
    *   `S`: Move tiles Down
    *   `D`: Move tiles Right
    *   `Q`: Quit the game
4.  **Goal:** Merge tiles to reach the `2048` tile.
5.  **Game Over:** The game ends if the board is full and no more merges are possible.

### Explanation of Key Parts:

*   **`initialize_game()`**: Sets up the 4x4 grid with all zeros and places two initial random tiles.
*   **`print_grid()`**: Clears the console and displays the current state of the board and the score. It uses f-strings for formatting to center the numbers.
*   **`get_empty_cells()` / `add_random_tile()`**: These work together to find available spots and place new `2`s (90% chance) or `4`s (10% chance).
*   **`_slide_row(row)`**: This is a crucial helper. It takes a list (representing a row or column) and moves all non-zero numbers to the beginning, filling the rest with zeros. Example: `[2, 0, 2, 4]` becomes `[2, 2, 4, 0]`.
*   **`_merge_row(row)`**: Another crucial helper. It iterates through a *slid* row and merges identical adjacent tiles (e.g., `[2, 2, 4, 0]` becomes `[4, 0, 4, 0]`). It also keeps track of the score added.
*   **`move(grid, direction)`**: This is the core logic for handling player input.
    *   It makes a `deepcopy` of the grid to compare later and see if any actual change occurred.
    *   For 'left' and 'right' moves, it applies `_slide_row` and `_merge_row` directly to each row (reversing for 'right').
    *   For 'up' and 'down' moves, it first `transpose`s the grid (swaps rows and columns), applies the row-based logic, and then `transpose`s it back. This avoids duplicating the slide/merge logic for columns.
    *   It returns the `new_grid`, `score_added`, and `moved_occurred` (a boolean indicating if the board actually changed).
*   **`check_win()`**: Simply iterates through the grid to see if `TARGET_TILE` (2048) is present.
*   **`check_lose()`**: This is a bit more complex. It first checks if there are any empty cells. If not, it then checks if any adjacent tiles (horizontally or vertically) are identical, which would allow a merge. If no empty cells and no possible merges, the game is lost.
*   **`main()`**: The main game loop that orchestrates everything: initializes, prints, gets input, processes moves, checks win/lose conditions, and repeats until the game ends.
