import numpy as np
from itertools import combinations


def find_antinodes(grid):
    height, width = grid.shape
    antennas = {}
    for i in range(height):
        for j in range(width):
            if grid[i, j] != ".":
                freq = grid[i, j]
                if freq not in antennas:
                    antennas[freq] = []
                antennas[freq].append((i, j))

    result = np.full_like(grid, ".")

    for freq, positions in antennas.items():
        if len(positions) < 2:
            continue

        for ant1, ant2 in combinations(positions, 2):
            y1, x1 = ant1
            y2, x2 = ant2

            dy = y2 - y1
            dx = x2 - x1

            if dx == 0:
                unit_dy = 1 if dy > 0 else -1
                unit_dx = 0
            elif dy == 0:
                unit_dy = 0
                unit_dx = 1 if dx > 0 else -1
            else:
                gcd = abs(np.gcd(dy, dx))
                unit_dy = dy // gcd
                unit_dx = dx // gcd

            y, x = y1, x1
            while 0 <= y < height and 0 <= x < width:
                result[y, x] = "#"
                y -= unit_dy
                x -= unit_dx

            y, x = y1, x1
            while 0 <= y < height and 0 <= x < width:
                result[y, x] = "#"
                y += unit_dy
                x += unit_dx

    return result


def load_grid(filename):
    with open(filename, "r") as f:
        lines = f.read().splitlines()
    return np.array([list(line) for line in lines])


grid = load_grid("08.txt")
result = find_antinodes(grid)
print("Result grid:")
for row in result:
    print("".join(row))
print("Antinodes count:", np.sum(result == "#"))
