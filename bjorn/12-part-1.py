import numpy as np
from collections import deque

if __name__ == "__main__":
    with open("12.txt") as f:
        grid = np.array([list(line.strip()) for line in f.readlines()])

    def find_regions(grid):
        rows, cols = grid.shape
        visited = set()
        regions = []

        def get_perimeter(region):
            perim = 0
            for r, c in region:
                for nr, nc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
                    if (
                        not (0 <= nr < rows and 0 <= nc < cols)
                        or (nr, nc) not in region
                    ):
                        perim += 1
            return perim

        def bfs(start_r, start_c):
            region = set()
            queue = deque([(start_r, start_c)])
            value = grid[start_r, start_c]
            while queue:
                r, c = queue.popleft()
                if (r, c) in region:
                    continue
                region.add((r, c))
                visited.add((r, c))
                for nr, nc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
                    if (
                        0 <= nr < rows
                        and 0 <= nc < cols
                        and grid[nr, nc] == value
                        and (nr, nc) not in visited
                    ):
                        queue.append((nr, nc))
            return region

        for r in range(rows):
            for c in range(cols):
                if (r, c) not in visited:
                    region = bfs(r, c)
                    regions.append(
                        {
                            "value": grid[r, c],
                            "coords": region,
                            "area": len(region),
                            "perimeter": get_perimeter(region),
                            "price": len(region) * get_perimeter(region),
                        }
                    )
        return regions

    regions = find_regions(grid)
    total_price = sum(region["price"] for region in regions)
    print(f"\nTotal price of fencing: {total_price}")
