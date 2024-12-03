import re

## Part 1


def part_1():
    with open("03.txt", "r") as file:
        content = file.read()

    pattern = r"mul\((\d+),(\d+)\)"
    matches = re.finditer(pattern, content)

    total = 0
    for match in matches:
        a = int(match.group(1))
        b = int(match.group(2))
        result = a * b
        total += result

    return total


part_1_result = part_1()
print(part_1_result)

## Part 2


def part_2():
    with open("03.txt", "r") as file:
        content = file.read()

    sections = re.split(r"(?:do\(\)|don\'t\(\))", content)
    commands = re.findall(r"(?:do\(\)|don\'t\(\))", content)

    # Implicitly add do() at the beginning
    commands.insert(0, "do()")

    mul_pattern = r"mul\((\d+),(\d+)\)"

    total = 0
    for command, section in zip(commands, sections):
        if command == "do()":
            matches = re.finditer(mul_pattern, section)
            for match in matches:
                a = int(match.group(1))
                b = int(match.group(2))
                result = a * b
                total += result

    return total


part_2_result = part_2()
print(part_2_result)
