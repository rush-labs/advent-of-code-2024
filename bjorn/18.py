import numpy as np
from collections import deque


def bfs_shortest_path(matrix):
    start, target = (0, 0), (matrix.shape[0] - 1,) * 2
    if not matrix[start] or not matrix[target]:
        return None
    predecessors = {start: None}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        if current == target:
            path = []
            while current:
                path.append((current[1], current[0]))
                current = predecessors[current]
            return path[::-1]
        for dy, dx in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_pos = (current[0] + dy, current[1] + dx)
            if (
                0 <= next_pos[0] < matrix.shape[0]
                and 0 <= next_pos[1] < matrix.shape[1]
                and matrix[next_pos]
                and next_pos not in predecessors
            ):
                predecessors[next_pos] = current
                queue.append(next_pos)
    return None


def check_paths_until_blocked(filename, size=71):
    matrix = np.ones((size, size), dtype=bool)
    coords = []

    with open(filename) as f:
        i = 0
        while True:
            line = f.readline().strip()
            if not line:
                break

            x, y = map(int, line.split(","))
            coords.append((x, y))

            if 0 <= x < size and 0 <= y < size:
                matrix[y, x] = False
                if i == 1023:
                    path = bfs_shortest_path(matrix)
                    if path:
                        print(f"Solution at 1024: path length = {len(path) - 1}")

                if i % 1000 == 0:
                    path = bfs_shortest_path(matrix)
                    print(
                        f"Checked {i} coordinates, path {'exists' if path else 'BLOCKED'}"
                    )

                if i >= 1024:
                    path = bfs_shortest_path(matrix)
                    if not path:
                        print(f"Path blocked after {i+1} coordinates")
                        print(f"Blocking coordinate: ({x}, {y})")
                        print("Previous 5 coordinates:")
                        for j in range(max(0, i - 4), i):
                            print(f"{j+1}: {coords[j]}")
                        return i
            i += 1

    print(f"Path remains possible after all {len(coords)} coordinates")
    return len(coords)


if __name__ == "__main__":
    final_count = check_paths_until_blocked("18.txt")
