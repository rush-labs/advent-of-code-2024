# Part 1


def is_safe(numbers, skip_idx=-1):
    rising = False
    falling = False
    prev = None

    for i in range(len(numbers)):
        if i == skip_idx:
            continue

        if prev is None:
            prev = numbers[i]
            continue

        curr = numbers[i]
        diff = curr - prev

        if abs(diff) < 1 or abs(diff) > 3:
            return False

        if diff > 0:
            if falling:
                return False
            rising = True
        elif diff < 0:
            if rising:
                return False
            falling = True

        prev = curr

    return True


with open("02.txt", "r") as file:
    safe_lines = 0
    for line in file:
        line = line.strip()
        if not line:
            continue
        numbers = line.split()
        numbers = list(map(int, numbers))
        safe = is_safe(numbers)
        if safe:
            safe_lines += 1
    print(safe_lines)


# Part 2


def is_safe_with_skip(numbers):
    if is_safe(numbers):
        return True

    for i in range(len(numbers)):
        if is_safe(numbers, skip_idx=i):
            return True

    return False


with open("02.txt", "r") as file:
    safe_lines = 0
    for line in file:
        line = line.strip()
        if not line:
            continue
        numbers = list(map(int, line.split()))
        if is_safe_with_skip(numbers):
            safe_lines += 1
    print(safe_lines)
