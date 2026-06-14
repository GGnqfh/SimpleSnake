# SimpleSnake Bug Fixes Documentation

## Overview
This document describes the bugs identified and fixed in the SimpleSnake game project.

## Bug Fixes Summary

| Bug ID | Severity | Description | Status |
|--------|----------|-------------|--------|
| BUG-001 | High | Recursive game restart causes potential stack overflow | Fixed |
| BUG-002 | High | Floating-point precision issues in collision detection | Fixed |
| BUG-003 | Medium | Resource cleanup on game exit | Fixed |

---

## Bug Details and Fixes

### BUG-001: Recursive Game Restart (High Severity)

**Problem**: When the player presses 'R' to restart the game after a game over, the code used recursive calls to `gameLoop()`. This could lead to stack overflow if the player restarts the game many times.

**Original Code (lines 82-84)**:
```python
if event.key == pygame.K_r:
    gameLoop()   # Restart
    return       # Exit current loop
```

**Root Cause**: Each restart creates a new stack frame, and Python has a default recursion depth limit (~1000).

**Fix Applied**: Changed the restart logic to use an outer `while True` loop instead of recursion.

**Fixed Code**:
```python
def gameLoop():
    while True:  # Outer loop for restarts
        game_over = False
        game_close = False
        # ... game logic ...
        
        while not game_over:
            # ... event handling ...
            if event.key == pygame.K_r:
                game_over = True  # Break inner loop, restart outer loop
                break
```

**Impact**: Prevents stack overflow, ensures memory stability during extended gameplay.

---

### BUG-002: Floating-Point Precision Issues (High Severity)

**Problem**: The `random_food()` function returned floating-point coordinates, but collision detection used exact equality comparisons. This could cause missed collisions due to floating-point precision errors.

**Original Code**:
```python
def random_food(snake_list):
    while True:
        fx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        fy = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
        if [fx, fy] not in snake_list:
            return fx, fy
```

**Root Cause**: Floating-point arithmetic introduces precision errors that can cause `x1 == foodx` to fail even when visually aligned.

**Fix Applied**: Added `int()` conversion to ensure all coordinates are integers.

**Fixed Code**:
```python
def random_food(snake_list):
    while True:
        fx = int(round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0)
        fy = int(round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0)
        if [fx, fy] not in snake_list:
            return fx, fy
```

Also changed initial position calculations to use integer division:
```python
x1 = dis_width // 2
y1 = dis_height // 2
```

**Impact**: Ensures reliable collision detection between snake and food.

---

### BUG-003: Resource Cleanup on Game Exit (Medium Severity)

**Problem**: The original code called `pygame.quit()` and `sys.exit()` multiple times in different code paths, which could lead to incomplete cleanup.

**Original Code**: Multiple scattered calls to `pygame.quit()` and `sys.exit()`.

**Fix Applied**: Consolidated exit logic to ensure proper resource cleanup sequence.

**Impact**: Ensures Pygame resources are properly released before program termination.

---

## Code Changes Summary

| File | Lines Changed | Change Type |
|------|--------------|-------------|
| snake.py | 41-42 | Added `int()` conversion for food coordinates |
| snake.py | 48 | Added outer `while True` loop |
| snake.py | 52-53 | Changed to integer division `//` |
| snake.py | 74-76 | Changed restart from recursion to loop exit |
| snake.py | 91-92 | Added break for outer loop restart |

---

## Testing Instructions

1. Install dependencies:
   ```bash
   pip install pygame
   ```

2. Run the game:
   ```bash
   python snake.py
   ```

3. Test scenarios:
   - Play the game normally (arrow keys or WASD)
   - Trigger game over by hitting walls or self
   - Press 'R' to restart (test multiple restarts)
   - Press 'Q' to quit from game over screen
   - Click window close button to exit

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.1 | 2026-06-14 | Fixed recursion, precision, and cleanup issues |
| 1.0.0 | Original | Initial release |

---

## License
This project is licensed under the MIT License - see the LICENSE file for details.