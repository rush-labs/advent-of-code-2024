from typing import List, Set, Tuple

Position = Tuple[int, int]
Direction = Tuple[int, int]
Grid = Set[Position]


def read_puzzle(filename: str) -> Tuple[List[str], str]:
    with open(filename, "r") as f:
        content = f.read()
    map_str, movements = content.split("\n\n")
    return map_str.strip().split("\n"), movements.strip()


def parse_map(map_lines: List[str]) -> Tuple[Position, Grid, Grid, int, int]:
    height = len(map_lines)
    width = len(map_lines[0])
    player_pos = None
    obstacles: Grid = set()
    walls: Grid = set()

    for y, line in enumerate(map_lines):
        for x, char in enumerate(line):
            if char == "@":
                player_pos = (x, y * 100)
            elif char == "O":
                obstacles.add((x, y * 100))
            elif char == "#":
                walls.add((x, y * 100))

    if player_pos is None:
        raise ValueError("No player position (@) found in map")

    return player_pos, obstacles, walls, width, height


def parse_movements(movement_str: str) -> List[Direction]:
    movement_map = {"^": (0, -100), "v": (0, 100), "<": (-1, 0), ">": (1, 0)}
    return [movement_map[char] for char in movement_str if char in movement_map]


def is_valid_position(pos: Position, walls: Grid, width: int, height: int) -> bool:
    x, y = pos
    return 0 <= x < width and 0 <= y < height * 100 and pos not in walls


def try_move(
    pos: Position,
    direction: Direction,
    obstacles: Grid,
    walls: Grid,
    width: int,
    height: int,
) -> Tuple[bool, Grid]:
    new_pos = (pos[0] + direction[0], pos[1] + direction[1])

    if not is_valid_position(new_pos, walls, width, height):
        return False, obstacles

    if new_pos not in obstacles:
        return True, obstacles

    push_pos = (new_pos[0] + direction[0], new_pos[1] + direction[1])

    if not is_valid_position(push_pos, walls, width, height):
        return False, obstacles

    if push_pos in obstacles:
        chain_success, new_obstacles = try_move(
            new_pos, direction, obstacles, walls, width, height
        )
        if not chain_success:
            return False, obstacles
        obstacles = new_obstacles

    new_obstacles = obstacles.copy()
    new_obstacles.remove(new_pos)
    new_obstacles.add(push_pos)
    return True, new_obstacles


def solve_puzzle(filename: str) -> List[Position]:
    map_lines, movement_str = read_puzzle(filename)
    player_pos, obstacles, walls, width, height = parse_map(map_lines)
    movements = parse_movements(movement_str)

    for direction in movements:
        success, new_obstacles = try_move(
            player_pos, direction, obstacles, walls, width, height
        )
        if success:
            player_pos = (player_pos[0] + direction[0], player_pos[1] + direction[1])
            obstacles = new_obstacles

    return sorted(list(obstacles))


if __name__ == "__main__":
    final_positions = solve_puzzle("15.txt")
    coordinate_sum = sum(x + y for x, y in final_positions)
    print(coordinate_sum)
