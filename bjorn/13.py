from dataclasses import dataclass
from z3 import *

position_x_offset = 10000000000000
position_y_offset = 10000000000000


@dataclass
class Vector2D:
    x: int
    y: int


@dataclass
class GameState:
    button_a: Vector2D
    button_b: Vector2D
    prize: Vector2D


def parse_input(filename):
    states = []
    with open(filename) as f:
        while True:
            a_line = f.readline().strip()
            if not a_line:
                break
            b_line = f.readline().strip()
            prize_line = f.readline().strip()

            a_parts = a_line.split(": ")[1].split(", ")
            button_a = Vector2D(
                int(a_parts[0].split("+")[1]), int(a_parts[1].split("+")[1])
            )

            b_parts = b_line.split(": ")[1].split(", ")
            button_b = Vector2D(
                int(b_parts[0].split("+")[1]), int(b_parts[1].split("+")[1])
            )

            prize_parts = prize_line.split(": ")[1].split(", ")
            prize = Vector2D(
                int(prize_parts[0].split("=")[1]) + position_x_offset,
                int(prize_parts[1].split("=")[1]) + position_y_offset,
            )

            states.append(GameState(button_a, button_b, prize))
            empty_line = f.readline()
            if not empty_line:
                break
    return states


def can_reach_position_z3(target, button_a, button_b):
    solver = Optimize()
    a_presses = Int("a_presses")
    b_presses = Int("b_presses")

    solver.add(a_presses >= 0)
    solver.add(b_presses >= 0)
    solver.add(button_a.x * a_presses + button_b.x * b_presses == target.x)
    solver.add(button_a.y * a_presses + button_b.y * b_presses == target.y)

    total_cost = 3 * a_presses + b_presses
    objective = solver.minimize(total_cost)

    if solver.check() == sat:
        model = solver.model()
        return (model[a_presses].as_long(), model[b_presses].as_long())
    return None


def calculate_total_cost(states):
    total_cost = 0
    for i, state in enumerate(states, 1):
        result = can_reach_position_z3(state.prize, state.button_a, state.button_b)
        if result is None:
            print(f"Prize {i} is unreachable!")
            continue
        a_count, b_count = result
        cost = a_count * 3 + b_count
        print(f"Prize {i}: {cost} tokens ({a_count} A presses, {b_count} B presses)")
        total_cost += cost
    return total_cost


if __name__ == "__main__":
    states = parse_input("13.txt")
    total_cost = calculate_total_cost(states)
    print(f"\nTotal tokens needed: {total_cost}")
