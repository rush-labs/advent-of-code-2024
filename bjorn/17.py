from z3 import *


def read_file():
    with open("17.txt") as f:
        lines = [l.strip() for l in f]
    regs = {"A": 0, "B": 0, "C": 0}
    for l in lines:
        if "Register" in l:
            reg, val = l.split(": ")
            regs[reg.split()[-1]] = int(val)
        elif "Program:" in l:
            program = [int(x) for x in l.split(": ")[1].split(",")]
    return regs, program


def get_val(op, regs, combo):
    return op if not combo or 0 <= op <= 3 else regs["ABC"[op - 4]]


def run_program(regs, prog):
    ip, out = 0, []
    while ip < len(prog) - 1:
        op, val = prog[ip], prog[ip + 1]
        if op == 0 and (p := get_val(val, regs, True)):
            regs["A"] //= 2**p
        elif op == 1:
            regs["B"] ^= val
        elif op == 2:
            regs["B"] = get_val(val, regs, True) % 8
        elif op == 3 and regs["A"]:
            ip = val
            continue
        elif op == 4:
            regs["B"] ^= regs["C"]
        elif op == 5:
            out.append(str(get_val(val, regs, True) % 8))
        elif op == 6 and (p := get_val(val, regs, True)):
            regs["B"] = regs["A"] // 2**p
        elif op == 7 and (p := get_val(val, regs, True)):
            regs["C"] = regs["A"] // 2**p
        ip += 2
    return ",".join(out) if out else None


def find_quine(prog):
    a = BitVec("a", 64)
    opt = Optimize()
    for i, t in enumerate(prog):
        s = i * 3
        v = LShR(a, s)
        m = v & 0b111
        x = m ^ 0b101
        f = (x ^ LShR(v, m ^ 0b001)) & 0b111
        opt.add(f == t)
    opt.add(a > 0)
    opt.minimize(a)
    return opt.model()[a].as_long() if opt.check() == sat else None


if __name__ == "__main__":
    try:
        regs, prog = read_file()
        print("Initial:", regs, "\nProgram:", prog)
        if out := run_program(regs, prog):
            print("Output:", out)
            if quine := find_quine(prog):
                print("Lowest quine:", quine)
        print("Final:", regs)
    except Exception as e:
        print(f"Error: {e}")
