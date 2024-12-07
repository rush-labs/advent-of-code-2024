from itertools import product
from operator import add as op_add, mul as op_multiply


def concat(a, b):
    return int(str(a) + str(b))


def evaluate(numbers, ops):
    result = numbers[0]
    for op, num in zip(ops, numbers[1:]):
        if op == op_add:
            result += num
        elif op == op_multiply:
            result *= num
        else:
            result = concat(result, num)
    return result


def format(numbers, ops, target):
    op_symbols = {op_add: " + ", op_multiply: " * ", concat: " || "}
    result = [str(numbers[0])]
    for num, op in zip(numbers[1:], ops):
        result.extend([op_symbols[op], str(num)])
    return f"{target} = {''.join(result)}"


def solve(filename):
    operators = [op_add, op_multiply, concat]
    total = solvable = unsolvable = 0

    with open(filename) as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            target, nums = line.split(":")
            target = int(target)
            numbers = [int(x) for x in nums.split()]

            if len(numbers) == 1:
                if numbers[0] == target:
                    total += target
                    solvable += 1
                else:
                    unsolvable += 1
                continue

            found = False
            for ops in product(operators, repeat=len(numbers) - 1):
                if evaluate(numbers, ops) == target:
                    print(format(numbers, ops, target))
                    total += target
                    solvable += 1
                    found = True
                    break

            if not found:
                print(f"{target} is not solvable")
                unsolvable += 1

    print(f"\nSummary:")
    print(f"Solvable equations: {solvable}")
    print(f"Unsolvable equations: {unsolvable}")
    print(f"Sum of all valid test values: {total}")

    return total, solvable, unsolvable


solve("07.txt")
