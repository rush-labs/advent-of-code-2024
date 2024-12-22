import heapq
from collections import defaultdict

EAST, NORTH, WEST, SOUTH = (0, 1), (-1, 0), (0, -1), (1, 0)
ROTATIONS = {
    EAST: [NORTH, SOUTH],
    NORTH: [WEST, EAST], 
    WEST: [SOUTH, NORTH],
    SOUTH: [EAST, WEST],
}

def read_maze(filename):
    with open(filename) as f:
        maze = [list(line.strip()) for line in f]
    start, end = None, None
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == "S":
                start = (i, j, EAST)
                maze[i][j] = "."
            elif maze[i][j] == "E":
                end = (i, j)
                maze[i][j] = "."
    return maze, start, end

def find_all_optimal_tiles(maze, start, end):
    frontier = [(0, start, {(start[0], start[1])})]
    min_costs = defaultdict(lambda: float("inf"))
    min_costs[start] = 0
    optimal_tiles = set()
    optimal_cost = float("inf")
    while frontier:
        cost, state, visited = heapq.heappop(frontier)
        row, col, direction = state
        if (row, col) == end:
            if cost < optimal_cost:
                optimal_cost = cost
                optimal_tiles = visited.copy()
            elif cost == optimal_cost:
                optimal_tiles.update(visited)
            continue
        if cost > optimal_cost:
            continue
        new_row, new_col = row + direction[0], col + direction[1]
        if 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]) and maze[new_row][new_col] == ".":
            new_state = (new_row, new_col, direction)
            new_cost = cost + 1
            if new_cost <= min_costs[new_state]:
                min_costs[new_state] = new_cost
                new_visited = visited | {(new_row, new_col)}
                heapq.heappush(frontier, (new_cost, new_state, new_visited))
        for new_dir in ROTATIONS[direction]:
            new_state = (row, col, new_dir)
            new_cost = cost + 1000
            if new_cost <= min_costs[new_state]:
                min_costs[new_state] = new_cost
                heapq.heappush(frontier, (new_cost, new_state, visited.copy()))
    return optimal_tiles, optimal_cost

def main():
    maze, start, end = read_maze("16.txt")
    optimal_tiles, optimal_cost = find_all_optimal_tiles(maze, start, end)
    print(f"Optimal path cost: {optimal_cost}")
    print(f"Number of tiles in optimal paths: {len(optimal_tiles)}")

if __name__ == "__main__":
    main()
