import numpy as np

EMPTY_TILE, OBSTACLE_TILE, GUARD_TILE = ".", "#", "^"
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Up, Right, Down, Left


def load_map(filename):
    with open(filename) as file:
        lines = file.readlines()
        max_length = max(len(line.strip()) for line in lines)
        return np.array(
            [list(line.strip().ljust(max_length, EMPTY_TILE)) for line in lines]
        )


def find_guard_position(map_array):
    y, x = np.where(map_array == GUARD_TILE)
    return int(y[0]), int(x[0])


def move(pos, direction, map_array):
    new_y = pos[0] + DIRECTIONS[direction][0]
    new_x = pos[1] + DIRECTIONS[direction][1]

    if (
        0 <= new_y < map_array.shape[0]
        and 0 <= new_x < map_array.shape[1]
        and map_array[new_y, new_x] != OBSTACLE_TILE
    ):
        return (new_y, new_x), direction

    return pos, (direction + 1) % 4


def is_guard_outside(pos, map_array):
    return pos[0] in (0, map_array.shape[0] - 1) or pos[1] in (
        0,
        map_array.shape[1] - 1,
    )


def create_path(map_array):
    pos = find_guard_position(map_array)
    direction = 0
    path = [pos]
    map_array[pos] = EMPTY_TILE

    while not is_guard_outside(pos, map_array):
        pos, direction = move(pos, direction, map_array)
        path.append(pos)

    return len(set(path))


print(create_path(load_map("06.txt")))
