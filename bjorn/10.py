import numpy as np
from collections import deque


def load_grid(filename):
    with open(filename, "r") as f:
        lines = f.read().splitlines()
        lines = [line.strip() for line in lines]
        lines = [line for line in lines if line]
    return np.array([list(map(int, line)) for line in lines])


def count_reachable_nines(grid):
    rows, cols = grid.shape
    directions = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])

    trailheads = np.argwhere(grid == 0)
    total_score = 0

    for start in trailheads:
        reachable_nines = set()
        queue = deque([(tuple(start), frozenset([tuple(start)]))])

        while queue:
            (current_row, current_col), visited = queue.popleft()
            current_height = grid[current_row, current_col]

            if current_height == 9:
                reachable_nines.add((current_row, current_col))
                continue

            next_positions = np.array([current_row, current_col]) + directions
            valid_mask = (
                (next_positions[:, 0] >= 0)
                & (next_positions[:, 0] < rows)
                & (next_positions[:, 1] >= 0)
                & (next_positions[:, 1] < cols)
            )

            valid_positions = next_positions[valid_mask]

            for next_row, next_col in valid_positions:
                next_pos = (next_row, next_col)
                if next_pos not in visited:
                    next_height = grid[next_row, next_col]
                    if next_height == current_height + 1:
                        new_visited = frozenset(visited | {next_pos})
                        queue.append((next_pos, new_visited))

        total_score += len(reachable_nines)

    return total_score


def main():
    grid = load_grid("10.txt")
    result = count_reachable_nines(grid)
    print(f"Sum of trailhead scores: {result}")


if __name__ == "__main__":
    main()
