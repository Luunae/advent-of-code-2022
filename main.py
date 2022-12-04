# Advent of Code 2022, Luna L Nova, assisted by GitHub Copilot.
# The first part of this file is code to run each part of each day's challenges.
# The second part of this file will be any helper functions needed on multiple days.
# Puzzle inputs will be found in /inputs

# ====================== Daily Challenges ======================
def day_01a():
    # The input is a list of numbers, one per line, with a group separated by a blank line.
    # The goal is to find the group with the highest sum, and return the sum.
    with open("inputs/01.txt") as f:
        data = f.read().splitlines()
    list_of_lists: list[list] = [[]]
    for i in range(len(data)):
        if data[i] != "":
            list_of_lists[-1].append(int(data[i]))
        if data[i] == "":
            list_of_lists.append([])
    highest_sum = 0
    for i in range(len(list_of_lists)):
        if sum(list_of_lists[i]) > highest_sum:
            highest_sum = sum(list_of_lists[i])
    return highest_sum


# ====================== Helper Functions ======================
# ====================== Daily Challenges ======================
# More of a scratch place to run each day's challenges. Edit as needed.
if __name__ == "__main__":
    print(day_01a())
