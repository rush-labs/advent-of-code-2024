# Part 1


def calc_distance(list_a, list_b):
    sorted_a = sorted(list_a)
    sorted_b = sorted(list_b)
    distance = 0
    for i in range(len(sorted_a)):
        distance += abs(sorted_a[i] - sorted_b[i])
    return distance


list_a = []
list_b = []
with open("01.txt", "r") as file:
    for line in file:
        line = line.strip()

        if not line:
            continue

        num1, num2 = map(int, line.split())
        list_a.append(num1)
        list_b.append(num2)

print(calc_distance(list_a, list_b))

# Part 2


def calc_similarity(list_a, list_b):
    similarity = 0
    for i in range(len(list_a)):
        value_a = list_a[i]
        count_b = list_b.count(value_a)
        similarity += value_a * count_b
    return similarity


print(calc_similarity(list_a, list_b))
