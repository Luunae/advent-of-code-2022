# Advent of Code 2022, Luna L Nova, assisted by GitHub Copilot.
# The first part of this file is code to run each part of each day's challenges.
# The second part of this file will be any helper functions needed on multiple days.
# Puzzle inputs will be found in /inputs

# ====================== Daily Challenges ======================
def day_01a():
    # The input is a list of numbers, one per line, with a group separated by a blank line.
    # The goal is to find the group with the highest sum, and return the sum.
    list_of_lists = create_list_of_lists_of_ints("inputs/01.txt")
    highest_sum = 0
    for i in range(len(list_of_lists)):
        if sum(list_of_lists[i]) > highest_sum:
            highest_sum = sum(list_of_lists[i])
    return highest_sum


def day_01b():
    list_of_lists = create_list_of_lists_of_ints("inputs/01.txt")
    # Get the highest three sums of the groups.
    highest_sums = [0, 0, 0]
    for i in range(len(list_of_lists)):
        if sum(list_of_lists[i]) > highest_sums[0]:
            highest_sums[0] = sum(list_of_lists[i])
            highest_sums.sort()
    return sum(highest_sums)


def day_02a():
    with open("inputs/02.txt") as f:
        data = f.read().splitlines()
    round_list = []
    for i in range(len(data)):
        if data[i] != "":
            round_list.append((data[i][0], data[i][2]))
    total_score = 0
    for element in round_list:
        total_score += score_rock_paper_scissors(element)
    return total_score


# ====================== Helper Functions ======================
def create_list_of_lists_of_ints(filename: str) -> list[list]:
    with open(filename) as f:
        data = f.read().splitlines()
    list_of_lists: list[list] = [[]]
    for i in range(len(data)):
        if data[i] != "":
            list_of_lists[-1].append(int(data[i]))
        if data[i] == "":
            list_of_lists.append([])
    return list_of_lists


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
    return score


# ====================== Daily Challenges ======================
# More of a scratch place to run each day's challenges. Edit as needed.
if __name__ == "__main__":
    print(day_02a())
