import numpy as np
from collections import deque


def find_regions(grid):
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    dR = [-1, 0, 1, 0]
    dC = [0, 1, 0, -1]

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def count_sides(r, c, value):
        sides = 0
        for i in range(4):
            new_r = r + dR[i]
            new_c = c + dC[i]

            if not is_valid(new_r, new_c) or grid[new_r, new_c] != value:
                r_90cc = r + dR[(i - 1) % 4]
                c_90cc = c + dC[(i - 1) % 4]
                is_begin_edge = (
                    not is_valid(r_90cc, c_90cc) or grid[r_90cc, c_90cc] != value
                )

                corner_r = new_r + dR[(i - 1) % 4]
                corner_c = new_c + dC[(i - 1) % 4]
                is_concave_begin = (
                    is_valid(corner_r, corner_c) and grid[corner_r, corner_c] == value
                )

                if is_begin_edge or is_concave_begin:
                    sides += 1

        return sides

    def bfs(start_r, start_c):
        region = set()
        queue = deque([(start_r, start_c)])
        value = grid[start_r, start_c]
        region_sides = 0

        while queue:
            r, c = queue.popleft()
            if (r, c) in region:
                continue

            region.add((r, c))
            visited[r, c] = True

            region_sides += count_sides(r, c, value)

            for dr, dc in zip(dR, dC):
                nr, nc = r + dr, c + dc
                if is_valid(nr, nc) and grid[nr, nc] == value and not visited[nr, nc]:
                    queue.append((nr, nc))

        return region, region_sides

    coords = np.where(~visited)
    for r, c in zip(coords[0], coords[1]):
        if not visited[r, c]:
            region, sides = bfs(r, c)
            regions.append(
                {
                    "value": grid[r, c],
                    "coords": region,
                    "area": len(region),
                    "sides": sides,
                    "price": len(region) * sides,
                }
            )

    return regions


if __name__ == "__main__":
    with open("12.txt") as f:
        grid = np.array([list(line.strip()) for line in f.readlines()])
    regions = find_regions(grid)
    total_price = sum(region["price"] for region in regions)
    print(f"\nTotal price of fencing: {total_price}")
