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
    return position[0] in (0, map.shape[0] - 1) or position[1] in (0, map.shape[1] - 1)


def trace_path(map):
    position = find_guard_position(map)
    direction = 0
    path = []
    seen_states = set()
    potential_hits = set()

    while True:
        state = (*position, direction)
        if state in seen_states:
            break
        if is_guard_outside(position, map):
            break

        seen_states.add(state)
        path.append(state)

        next_position = (
            position[0] + DIRECTIONS[direction][0],
            position[1] + DIRECTIONS[direction][1],
        )
        if (
            0 <= next_position[0] < map.shape[0]
            and 0 <= next_position[1] < map.shape[1]
            and map[next_position] == EMPTY_TILE
        ):
            potential_hits.add(next_position)

        position, direction = move(position, direction, map)

    return path, potential_hits


def find_loops_smart(map):
    original_path, potential_hits = trace_path(map)
    loop_positions = set()

    print(
        f"Testing {len(potential_hits)} potential positions (instead of {np.sum(map == EMPTY_TILE)})"
    )

    for potential_position in potential_hits:
        test_map = map.copy()
        test_map[potential_position] = OBSTACLE_TILE

        position = find_guard_position(test_map)
        direction = 0
        seen_states = {}
        step = 0

        while True:
            state = (*position, direction)
            if state in seen_states:
                loop_positions.add(potential_position)
                break

            if is_guard_outside(position, test_map):
                break

            seen_states[state] = step
            step += 1
            position, direction = move(position, direction, test_map)

    return sorted(loop_positions)


map_data = load_map("06.txt")
loop_positions = find_loops_smart(map_data)
print(f"Found {len(loop_positions)} loop positions")
