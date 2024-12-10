def compute_initial(input):
    result = []
    block_num = 0
    for i in range(0, len(input) - 1, 2):
        result.extend([block_num] * int(input[i]) + [-1] * int(input[i + 1]))
        block_num += 1
    if len(input) % 2:
        result.extend([block_num] * int(input[-1]))
    return result


def compress(s):
    steps = [s.copy()]

    blocks = {}
    for i, num in enumerate(s):
        if num != -1:
            blocks.setdefault(num, []).append(i)

    for block_id in sorted(blocks.keys(), reverse=True):
        positions = blocks[block_id]
        block_size = positions[-1] - positions[0] + 1
        block = s[positions[0] : positions[-1] + 1]

        free_spaces = []
        start = -1
        count = 0

        for i in range(positions[0]):
            if s[i] == -1:
                if start == -1:
                    start = i
                count += 1
            else:
                if start != -1:
                    free_spaces.append((start, count))
                start = -1
                count = 0

        if start != -1:
            free_spaces.append((start, count))

        for start, size in free_spaces:
            if size >= block_size:
                new_s = s.copy()
                new_s[start : start + block_size] = block
                new_s[positions[0] : positions[-1] + 1] = [-1] * block_size
                s = new_s
                steps.append(s.copy())
                break

    final = [None if x == -1 else x for x in s]
    steps.append(final)
    return steps


def process_file(filename):
    with open(filename) as file:
        input = file.read().strip()
        final = compress(compute_initial(input))[-1]
        return sum(i * num for i, num in enumerate(final) if num is not None)


print(process_file("09.txt"))
