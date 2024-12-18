import numpy as np
import matplotlib.pyplot as plt


class Entity:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def update(self, width, height, seconds):
        self.x = (self.x + self.vx * seconds) % width
        self.y = (self.y + self.vy * seconds) % height


def parse_line(line):
    pos, vel = line.strip().split(" ")
    px, py = map(int, pos[2:].split(","))
    vx, vy = map(int, vel[2:].split(","))
    return (px, py, vx, vy)


def create_entity_map(entities, width, height):
    entity_map = np.zeros((height, width))
    for x, y, _, _ in entities:
        entity_map[int(y), int(x)] += 1
    return entity_map


def save_visualization(entity_map, second):
    plt.figure(figsize=(10, 10))
    plt.imshow(entity_map, cmap="viridis")
    plt.colorbar(label="Number of entities")
    plt.title(f"Entity positions at second {second}")
    plt.savefig("14.png")
    plt.close()


def check_alignments(entities, width, height, t):
    next_set = set()
    matching = set()

    for px, py, vx, vy in entities:
        xf, yf = (px + t * vx) % width, (py + t * vy) % height
        if (xf, yf) in next_set:
            matching.add((xf, yf))
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                next_x = (xf + dx) % width
                next_y = (yf + dy) % height
                next_set.add((next_x, next_y))

    return len(matching), next_set


def simulate_and_detect(filename, width, height, max_seconds, save_interval=100):
    with open(filename, "r") as f:
        entities = [parse_line(line) for line in f]

    significant_moments = []

    for t in range(max_seconds):
        match_count, next_set = check_alignments(entities, width, height, t)

        if match_count > 256:
            significant_moments.append((t, match_count))

            entity_positions = []
            for px, py, vx, vy in entities:
                xf = (px + t * vx) % width
                yf = (py + t * vy) % height
                entity_positions.append((xf, yf))

            entity_map = create_entity_map(
                [(x, y, 0, 0) for x, y in entity_positions], width, height
            )
            save_visualization(entity_map, t)

            print(f"\nSignificant alignment detected at second {t}")
            print(f"Number of matching positions: {match_count}")

        if t % save_interval == 0:
            print(f"Processed second {t}/{max_seconds}")

    return significant_moments


significant_moments = simulate_and_detect("14.txt", 101, 103, 10000, save_interval=100)

print("\nFinal Report:")
print(f"Found {len(significant_moments)} significant alignment moments:")
for t, count in significant_moments:
    print(f"Second {t}: {count} matching positions")
