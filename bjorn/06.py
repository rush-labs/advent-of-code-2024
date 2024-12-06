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


def find_guard_position(map):
    y, x = np.where(map == GUARD_TILE)
    return int(y[0]), int(x[0])


def move(position, direction, map):
    new_y = position[0] + DIRECTIONS[direction][0]
    new_x = position[1] + DIRECTIONS[direction][1]

    if (
        0 <= new_y < map.shape[0]
        and 0 <= new_x < map.shape[1]
        and map[new_y, new_x] != OBSTACLE_TILE
    ):
        return (new_y, new_x), direction

    return position, (direction + 1) % 4


def is_guard_outside(position, map):
    return position[0] in (0, map.shape[0] - 1) or position[1] in (
        0,
        map.shape[1] - 1,
    )


def create_path(map):
    position = find_guard_position(map)
    direction = 0
    path = [position]
    map[position] = EMPTY_TILE

    while not is_guard_outside(position, map):
        position, direction = move(position, direction, map)
        path.append(position)

    return len(set(path))


print(create_path(load_map("06.txt")))
