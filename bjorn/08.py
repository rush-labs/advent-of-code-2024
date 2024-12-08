import numpy as np
from itertools import combinations


def find_antinodes(grid):
    height, width = grid.shape
    # Map frequency letters to their antenna positions
    antennas = {}
    for i in range(height):
        for j in range(width):
            if grid[i, j] != ".":
                freq = grid[i, j]
                if freq not in antennas:
                    antennas[freq] = []
                antennas[freq].append((i, j))

    # Copy input grid to mark results
    result = np.full_like(grid, ".")
    for i in range(height):
        for j in range(width):
            if grid[i, j] != ".":
                result[i, j] = grid[i, j]

    # For each frequency pair, mark antinodes beyond each antenna
    for freq, positions in antennas.items():
        if len(positions) < 2:
            continue
        for ant1, ant2 in combinations(positions, 2):
            dy = ant2[0] - ant1[0]
            dx = ant2[1] - ant1[1]
            antinode1 = (ant2[0] + dy, ant2[1] + dx)  # Beyond ant2
            antinode2 = (ant1[0] - dy, ant1[1] - dx)  # Before ant1

            for y, x in [antinode1, antinode2]:
                if 0 <= y < height and 0 <= x < width:
                    if grid[y, x] != freq:
                        result[y, x] = "#"
    return result


def load_grid(filename):
    # Read grid from file into numpy array
    with open(filename, "r") as f:
        lines = f.read().splitlines()
    grid = np.array([list(line) for line in lines])
    return grid


# Process grid and count antinodes
grid = load_grid("08.txt")
result = find_antinodes(grid)
print("Result grid:")
for row in result:
    print("".join(row))
print("Antinodes count:", np.sum(result == "#"))
