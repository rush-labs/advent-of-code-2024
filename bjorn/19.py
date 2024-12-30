def parse_input(filename):
    with open(filename) as f:
        patterns, designs = f.read().strip().split("\n\n")
        patterns = patterns.split(", ")
        designs = designs.strip().split("\n")
    return patterns, designs


def count_construction_ways(design, patterns, memo=None):
    if memo is None:
        memo = {}

    if not design:
        return 1
    if design in memo:
        return memo[design]

    total_ways = 0
    for pattern in patterns:
        if design.startswith(pattern):
            remaining = design[len(pattern) :]
            total_ways += count_construction_ways(remaining, patterns, memo)

    memo[design] = total_ways
    return total_ways


def analyze_designs(patterns, designs):
    possible_count = 0
    total_permutations = 0
    design_ways = {}

    for design in designs:
        ways = count_construction_ways(design, patterns)
        if ways > 0:
            possible_count += 1
            total_permutations += ways
        design_ways[design] = ways

    return possible_count, total_permutations, design_ways


def main():
    patterns, designs = parse_input("19.txt")
    possible_count, total_perms, design_ways = analyze_designs(patterns, designs)

    print(f"Possible designs: {possible_count}")
    print(f"Total permutations: {total_perms}")


if __name__ == "__main__":
    main()
