import networkx as nx


def fix_update(update, rules):
    G = nx.DiGraph()
    G.add_nodes_from(update)

    for rule in rules:
        if rule[0][0] in update and rule[1][0] in update:
            G.add_edge(rule[0][0], rule[1][0])

    try:
        return list(nx.topological_sort(G))
    except nx.NetworkXUnfeasible:
        return None


with open("05.txt", "r") as file:
    text = file.read()
    paragraphs = text.split("\n\n")
    paragraphs = [p.strip() for p in paragraphs]
    paragraphs = [p for p in paragraphs if p]

    rules = [
        [tuple(map(int, r.strip().split())) for r in line.split("|")]
        for line in paragraphs[0].split("\n")
    ]

    updates = [[int(u) for u in line.split(",")] for line in paragraphs[1].split("\n")]

    valid_updates = []
    fixed_updates = []

    for update in updates:
        relevant_rules = [
            rule for rule in rules if rule[0][0] in update and rule[1][0] in update
        ]

        is_valid = all(
            update.index(rule[0][0]) < update.index(rule[1][0])
            for rule in relevant_rules
        )

        if is_valid:
            valid_updates.append(update)
        else:
            fixed = fix_update(update, relevant_rules)
            if fixed:
                fixed_updates.append(fixed)

    part_1_total = sum(update[len(update) // 2] for update in valid_updates)
    part_2_total = sum(update[len(update) // 2] for update in fixed_updates)

    print(part_1_total)
    print(part_2_total)
