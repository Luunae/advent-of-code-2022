# Advent of Code 2022, Luna L Nova, assisted by GitHub Copilot.
# The first part of this file is code to run each part of each day's challenges.
# The second part of this file will be any helper functions needed on multiple days.
# Puzzle inputs will be found in /inputs

# ====================== Daily Challenges ======================
def day_01a():
    # The input is a list of numbers, one per line, with a group separated by a blank line.
    # The goal is to find the group with the highest sum, and return the sum.
    list_of_lists = prepare_day_one()
    highest_sum = 0
    for i in range(len(list_of_lists)):
        if sum(list_of_lists[i]) > highest_sum:
            highest_sum = sum(list_of_lists[i])
    return highest_sum


def day_01b():
    list_of_lists = prepare_day_one()
    # Get the highest three sums of the groups.
    highest_sums = [0, 0, 0]
    for i in range(len(list_of_lists)):
        if sum(list_of_lists[i]) > highest_sums[0]:
            highest_sums[0] = sum(list_of_lists[i])
            highest_sums.sort()
    return sum(highest_sums)


def day_02a():
    round_list = prepare_day_two()
    total_score = 0
    for element in round_list:
        total_score += score_rock_paper_scissors(element)
    return total_score


def day_02b():
    round_list = prepare_day_two()
    total_score = 0
    for element in round_list:
        total_score += rig_rock_paper_scissors(element)
    return total_score


def day_03a():
    rucksacks = prepare_simple_input("inputs/03.txt")
    # Make a lambda function to split each string in rucksacks into a tuple of two strings at the halfway point.
    rucksacks = list(map(lambda x: (x[: len(x) // 2], x[len(x) // 2 :]), rucksacks))
    priority_sum = 0
    for rucksack in rucksacks:
        for letter in rucksack[0]:
            if letter in rucksack[1]:
                priority_sum += rucksack_valuation(letter)
                break
    return priority_sum


def day_03b():
    rucksacks = prepare_simple_input("inputs/03.txt")
    groups = []
    # Group each three rucksacks together in a tuple in the groups list.
    for i in range(0, len(rucksacks), 3):
        groups.append((rucksacks[i], rucksacks[i + 1], rucksacks[i + 2]))
    priority_sum = 0
    for group in groups:
        for letter in group[0]:
            if letter in group[1] and letter in group[2]:
                priority_sum += rucksack_valuation(letter)
                break
    return priority_sum


def day_04a():
    assignment_list = prepare_simple_input("inputs/04.txt")
    groups = []
    for line in assignment_list:
        if line != "":
            first, second = line.split(",")
            a, b = first.split("-")
            c, d = second.split("-")
            groups.append((int(a), int(b), int(c), int(d)))
    fully_contained_groups = 0
    for group in groups:
        if group[0] <= group[2] and group[1] >= group[3]:
            fully_contained_groups += 1
        elif group[0] >= group[2] and group[1] <= group[3]:
            fully_contained_groups += 1
    return fully_contained_groups


# ====================== Helper Functions ======================
def prepare_simple_input(filename: str) -> list:
    with open(filename) as f:
        data = f.read().splitlines()
    return data


def prepare_day_one() -> list[list]:
    with open("inputs/01.txt") as f:
        data = f.read().splitlines()
    list_of_lists: list[list] = [[]]
    for i in range(len(data)):
        if data[i] != "":
            list_of_lists[-1].append(int(data[i]))
        if data[i] == "":
            list_of_lists.append([])
    return list_of_lists


def prepare_day_two():
    with open("inputs/02.txt") as f:
        data = f.read().splitlines()
    round_list = []
    for i in range(len(data)):
        if data[i] != "":
            round_list.append((data[i][0], data[i][2]))
    return round_list


def score_rock_paper_scissors(choices: tuple) -> int:
    score = 0
    # Make a name to point relationship. "A" is 1 point, "B" is 2 points, C is 3 points.
    # X is also 1 point, Y is 2 points, Z is 3 points.
    name_points = {"A": 1, "B": 2, "C": 3, "X": 1, "Y": 2, "Z": 3}
    winning_choices: list[tuple] = [("A", "Y"), ("B", "Z"), ("C", "X")]
    if name_points[choices[0]] == name_points[choices[1]]:  # Tie
        score += 3
    elif choices in winning_choices:  # Player wins
        score += 6
    else:  # Computer wins
        score += 0  # Don't technically need this, but it's here for clarity.
    score += name_points[choices[1]]
    print(score)
    return score


def rig_rock_paper_scissors(prompt: tuple) -> int:
    # Make a name to point relationship. "A" is 1 point, "B" is 2 points, C is 3 points.
    # X is also 1 point, Y is 2 points, Z is 3 points.
    print(prompt)
    position = {"A": 0, "B": 1, "C": 2}
    winning_outcomes: list[tuple] = [("A", "Y"), ("B", "Z"), ("C", "X")]
    tying_outcomes: list[tuple] = [("A", "X"), ("B", "Y"), ("C", "Z")]
    losing_outcomes: list[tuple] = [("A", "Z"), ("B", "X"), ("C", "Y")]
    # Holy crap those were all autogenerated after typing "winning", "tying", and "losing".
    if prompt[1] == "Z":  # We should win, select that branch.
        print("Winning")
        outcome = winning_outcomes[position[prompt[0]]]
        return score_rock_paper_scissors(outcome)
    elif prompt[1] == "Y":  # We should tie, select that branch.
        print("Tying")
        outcome = tying_outcomes[position[prompt[0]]]
        return score_rock_paper_scissors(outcome)
    elif prompt[1] == "X":  # We should lose, select that branch.
        print("Losing")
        outcome = losing_outcomes[position[prompt[0]]]
        return score_rock_paper_scissors(outcome)


def rucksack_valuation(character: str) -> int:
    # ord('a') - 96 = 1
    # ord('A') - 38 = 27
    if len(character) != 1:
        raise ValueError("Character must be a single letter.")
    if not character.isalpha():
        raise ValueError("Character must be alphabetical.")
    if character.islower():
        return ord(character) - 96
    else:
        return ord(character) - 38


# ====================== Daily Challenges ======================
# More of a scratch place to run each day's challenges. Edit as needed.
if __name__ == "__main__":
    print(day_04a())
