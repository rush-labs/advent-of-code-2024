def compute_initial(input):
    result = ""
    block_num = 0
    for i in range(0, len(input) - 1, 2):
        result += chr(0x30 + block_num) * int(input[i]) + "." * int(input[i + 1])
        block_num += 1
    if len(input) % 2:
        result += chr(0x30 + block_num) * int(input[-1])
    return result


def compress(s):
    steps = [s]
    while "." in s:
        last_val_pos = next(
            (i for i in range(len(s) - 1, -1, -1) if s[i] not in "." + " "), None
        )
        if last_val_pos is None:
            s = s.replace(".", " ")
            steps.append(s)
            break
        first_dot_pos = s.find(".")
        if first_dot_pos != -1 and first_dot_pos < last_val_pos:
            s = (
                s[:first_dot_pos]
                + s[last_val_pos]
                + s[first_dot_pos + 1 : last_val_pos]
                + s[last_val_pos + 1 :]
            )
            steps.append(s)
        else:
            s = s.replace(".", " ")
            steps.append(s)
            break
    return steps


def process_file(filename):
    with open(filename) as file:
        input = file.read().strip()
        final = compress(compute_initial(input))[-1]
        return sum(i * (ord(c) - 0x30) for i, c in enumerate(final) if c not in ". ")


print(process_file("09.txt"))
