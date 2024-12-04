import numpy as np


def find_target(grid, target):
    directions = np.array(
        [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
    )
    rows, cols = len(grid), len(grid[0])
    target_len = len(target)
    count = 0
    np_grid = np.array(grid)

    for di, dj in directions:
        if di > 0:
            max_i = rows - di * (target_len - 1)
        elif di < 0:
            max_i = rows + abs(di) * (target_len - 1)
        else:
            max_i = rows

        if dj > 0:
            max_j = cols - dj * (target_len - 1)
        elif dj < 0:
            max_j = cols + abs(dj) * (target_len - 1)
        else:
            max_j = cols

        for i in range(max(0, -di * (target_len - 1)), max_i):
            for j in range(max(0, -dj * (target_len - 1)), max_j):
                indices_i = i + di * np.arange(target_len)
                indices_j = j + dj * np.arange(target_len)

                if (
                    (0 <= indices_i).all()
                    and (indices_i < rows).all()
                    and (0 <= indices_j).all()
                    and (indices_j < cols).all()
                ):
                    word = "".join(np_grid[indices_i, indices_j])
                    if word == target:
                        count += 1

    return count


def find_x_mas(grid):
    a_mask = grid == "A"
    valid_mask = a_mask[1:-1, 1:-1]

    valid_positions = np.argwhere(valid_mask)
    valid_positions += 1

    diag1_top = grid[valid_positions[:, 0] - 1, valid_positions[:, 1] - 1]
    diag1_bottom = grid[valid_positions[:, 0] + 1, valid_positions[:, 1] + 1]

    diag2_top = grid[valid_positions[:, 0] - 1, valid_positions[:, 1] + 1]
    diag2_bottom = grid[valid_positions[:, 0] + 1, valid_positions[:, 1] - 1]

    diag1_strings = np.char.add(np.char.add(diag1_top, "A"), diag1_bottom)
    diag2_strings = np.char.add(np.char.add(diag2_top, "A"), diag2_bottom)

    valid_patterns = ((diag1_strings == "MAS") | (diag1_strings == "SAM")) & (
        (diag2_strings == "MAS") | (diag2_strings == "SAM")
    )

    return np.sum(valid_patterns)


with open("04.txt") as f:
    lines = f.read().strip().split("\n")
    grid = np.array([list(line) for line in lines])

print("XMAS instances:", find_target(grid, "XMAS"))
print("X-MAS instances:", find_x_mas(grid))
