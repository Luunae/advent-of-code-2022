# Advent of Code 2022, Luna L Nova, assisted by GitHub Copilot.
# The first part of this file is code to run each part of each day's challenges.
# The second part of this file will be any helper functions needed on multiple days.
# Puzzle inputs will be found in /inputs

# ====================== Daily Challenges ======================
def day_01a():
    # The input is a list of numbers, one per line, with a group separated by a blank line.
    # The goal is to find the group with the highest sum, and return the sum.
    list_of_lists = create_list_of_lists("inputs/01.txt")
    highest_sum = 0
    for i in range(len(list_of_lists)):
        if sum(list_of_lists[i]) > highest_sum:
            highest_sum = sum(list_of_lists[i])
    return highest_sum


def day_01b():
    list_of_lists = create_list_of_lists("inputs/01.txt")
    # Get the highest three sums of the groups.
    highest_sums = [0, 0, 0]
    for i in range(len(list_of_lists)):
        if sum(list_of_lists[i]) > highest_sums[0]:
            highest_sums[0] = sum(list_of_lists[i])
            highest_sums.sort()
    return sum(highest_sums)


# ====================== Helper Functions ======================
def create_list_of_lists(filename: str) -> list[list]:
    with open(filename) as f:
        data = f.read().splitlines()
    list_of_lists: list[list] = [[]]
    for i in range(len(data)):
        if data[i] != "":
            list_of_lists[-1].append(int(data[i]))
        if data[i] == "":
            list_of_lists.append([])
    return list_of_lists


# ====================== Daily Challenges ======================
# More of a scratch place to run each day's challenges. Edit as needed.
if __name__ == "__main__":
    print(day_01b())
