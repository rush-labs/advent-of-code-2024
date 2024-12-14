from collections import Counter
from typing import List, Dict


def transform(stones_counter: Counter) -> Counter:
    new_counter = Counter()
    for stone, count in stones_counter.items():
        if stone == 0:
            new_counter[1] += count
            continue
        digits = str(stone)
        if len(digits) % 2 == 0:
            mid = len(digits) // 2
            new_counter[int(digits[:mid])] += count
            new_counter[int(digits[mid:])] += count
            continue
        new_counter[stone * 2024] += count
    return new_counter


def simulate(initial_stones: List[int], blinks: int) -> int:
    stones_counter = Counter(initial_stones)
    seen_states: Dict[tuple, int] = {}

    for blink in range(blinks):
        current_state = tuple(sorted(stones_counter.items()))
        if current_state in seen_states:
            cycle_length = blink - seen_states[current_state]
            remaining_blinks = (blinks - blink) % cycle_length
            for _ in range(remaining_blinks):
                stones_counter = transform(stones_counter)
            return sum(stones_counter.values())
        seen_states[current_state] = blink
        stones_counter = transform(stones_counter)
    return sum(stones_counter.values())


if __name__ == "__main__":
    with open("11.txt") as f:
        initial_stones = [int(x) for x in f.readline().split()]
        print(simulate(initial_stones, 75))
