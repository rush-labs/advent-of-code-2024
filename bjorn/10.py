import numpy as np
from collections import deque
from typing import List, Set, Tuple, Dict


def load_grid(filename):
    with open(filename, "r") as f:
        lines = f.read().splitlines()
        lines = [line.strip() for line in lines]
        lines = [line for line in lines if line]
    return np.array([list(map(int, line)) for line in lines])


def count_reachable_nines_and_paths(grid):
    rows, cols = grid.shape
    directions = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
    trailheads = np.argwhere(grid == 0)

    total_unique_nines = 0
    all_paths: Dict[Tuple[int, int], List[List[Tuple[int, int]]]] = {}

    for start in trailheads:
        start_pos = tuple(start)
        reachable_nines = set()
        all_paths[start_pos] = []

        queue = deque([(start_pos, frozenset([start_pos]), [start_pos])])

        while queue:
            current_pos, visited, current_path = queue.popleft()
            current_row, current_col = current_pos
            current_height = grid[current_row, current_col]

            if current_height == 9:
                reachable_nines.add(current_pos)
                all_paths[start_pos].append(current_path)
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
                        new_path = current_path + [next_pos]
                        queue.append((next_pos, new_visited, new_path))

        total_unique_nines += len(reachable_nines)

    total_valid_paths = sum(len(paths) for paths in all_paths.values())

    return total_unique_nines, total_valid_paths


grid = load_grid("10.txt")
unique_nines, valid_paths = count_reachable_nines_and_paths(grid)
print(f"Sum of unique reachable nines from each start: {unique_nines}")
print(f"Total number of valid paths: {valid_paths}")
