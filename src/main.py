# Advent of Code 2022, Luna L Nova, assisted by GitHub Copilot.
# The first part of this file is code to run each part of each day's challenges.
# The second part of this file will be any helper functions needed on multiple days.
# Puzzle inputs will be found in /inputs
from enum import Enum
import sys


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
    rucksacks = prepare_simple_input("inputs/03.dat")
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
    rucksacks = prepare_simple_input("inputs/03.dat")
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
    groups = prepare_day_four()
    fully_contained_groups = 0
    for group in groups:
        if group[0] <= group[2] and group[1] >= group[3]:
            fully_contained_groups += 1
        elif group[0] >= group[2] and group[1] <= group[3]:
            fully_contained_groups += 1
    return fully_contained_groups


def day_04b():
    groups = prepare_day_four()
    overlapping_ranges = 0
    for group in groups:
        if (
            (group[2] <= group[0] <= group[3])
            or (group[2] <= group[1] <= group[3])
            or (group[0] <= group[2] and group[1] >= group[3])
            or (group[0] >= group[2] and group[1] <= group[3])
        ):
            overlapping_ranges += 1
    return overlapping_ranges


def day_05a():
    preparations: tuple[list, list] = prepare_day_five()
    stacks, instructions = preparations
    for command in instructions:
        for i in range(int(command[0])):
            stacks[command[2]].append(stacks[command[1]].pop())
    final_word = ""
    for stack in stacks:
        final_word += stack[-1]
    return final_word


def day_05b():
    preparations: tuple[list, list] = prepare_day_five()
    stacks, instructions = preparations
    for command in instructions:
        # Move the last command[0] elements from stack[command[1]] to stack[command[2]]
        number_of_moves = command[0]
        for i in range(command[0]):
            stacks[command[2]].append(stacks[command[1]].pop(-number_of_moves + i))
    final_word = ""
    for stack in stacks:
        final_word += stack[-1]
    return final_word


def day_06a():
    signal = prepare_simple_input("inputs/06.dat")[0]
    return find_first_signal_marker(signal, "START_OF_PACKET")


def day_06b():
    signal = prepare_simple_input("inputs/06.dat")[0]
    return find_first_signal_marker(signal, "START_OF_MESSAGE")


def day_07a():
    filetree = prepare_day_seven("inputs/07-example.dat")
    return traverse_sum_sizes(filetree.directories, 100_000, True)


def day_07b():
    total_space = 70_000_000
    space_needed = 30_000_000
    filetree = prepare_day_seven("inputs/07.dat")
    current_space_taken = sum_file_sizes(filetree.directories)
    space_to_remove = space_needed - (total_space - current_space_taken)
    print(f"Total space: {total_space}")
    print(f"Current space taken: {current_space_taken}")
    print(f"Space needed: {space_needed}")
    print(f"Space left: {total_space - current_space_taken}")
    directories = create_list_of_directories("", filetree.directories, [])
    directories = sorted(directories, key=lambda x: x[1], reverse=False)
    print(directories)
    for directory in directories:
        if directory[1] >= space_to_remove:
            return directory[1]


# ======================= Helper Classes =======================
class Filesystem:
    def __init__(self):
        self.directories = {}
        self.current_directory = ""

    def add_directory(self, directory_name: str):
        location = self.current_directory.split("/")
        while "" in location:
            location.remove("")
        current_directory = self.directories
        while location:
            part = location.pop(0)
            current_directory = current_directory[part]
        current_directory[directory_name] = {}

    def cd(self, directory_name: str):
        if directory_name == "..":
            self.current_directory = self.current_directory[:-1]
            while self.current_directory[-1] != "/":
                self.current_directory = self.current_directory[:-1]
        else:
            # I think I need to rebuild the nested dictionary trick here.
            location = self.current_directory.split("/")
            while "" in location:
                location.remove("")
            current_directory = self.directories
            while location:
                part = location.pop(0)
                try:
                    current_directory = current_directory[part]
                except:  # Haha, fuck.
                    continue
            if directory_name in current_directory:
                self.current_directory += directory_name + "/"
            else:
                self.add_directory(directory_name)
                self.current_directory += directory_name + "/"

    def add_file(
        self, file_size: int, file_name: str
    ):  # Mimic the behaviour of the AoC input.
        location = self.current_directory.split("/")
        # a/b/c -> ["a", "b", "c"]
        # directories = {"a": {"b": {"c": {}}}}}
        while "" in location:
            location.remove("")
        current_directory = self.directories
        while location:
            part = location.pop(0)
            current_directory = current_directory[part]
        current_directory[file_name] = file_size


# ====================== Helper Functions ======================
def prepare_simple_input(filename: str) -> list:
    with open(filename) as f:
        data = f.read().splitlines()
    return data


def prepare_day_one() -> list[list]:
    with open("inputs/01.dat") as f:
        data = f.read().splitlines()
    list_of_lists: list[list] = [[]]
    for i in range(len(data)):
        if data[i] != "":
            list_of_lists[-1].append(int(data[i]))
        if data[i] == "":
            list_of_lists.append([])
    return list_of_lists


def prepare_day_two():
    with open("inputs/02.dat") as f:
        data = f.read().splitlines()
    round_list = []
    for i in range(len(data)):
        if data[i] != "":
            round_list.append((data[i][0], data[i][2]))
    return round_list


def prepare_day_four():
    assignment_list = prepare_simple_input("inputs/04.dat")
    groups = []
    for line in assignment_list:
        if line != "":
            first, second = line.split(",")
            a, b = first.split("-")
            c, d = second.split("-")
            groups.append((int(a), int(b), int(c), int(d)))
    return groups


def prepare_day_five():
    puzzle_input = prepare_simple_input("inputs/05.dat")
    number_of_stacks = 0
    for row in puzzle_input:
        if row[1] == "1":
            number_of_stacks = row[-2]
            break
    stacks = []
    for i in range(int(number_of_stacks)):
        stacks.append([])
    for row in puzzle_input:
        if row[1] == "1":
            break
        for character in range(1, (len(row) - 1), 4):
            if row[character] != " ":
                stacks[character // 4].insert(0, row[character])
    instructions = []
    for line in puzzle_input:
        if line == "":
            continue
        if line[0] == "m":
            # I hate data mangling I hate data mangling I hate data mangling.
            piece_a = list(line.split(" "))
            piece_b = [int(piece_a[1]), int(piece_a[3]) - 1, int(piece_a[5]) - 1]
            instructions.append(tuple(piece_b))
    combined_data = (stacks, instructions)
    return combined_data


def prepare_day_seven(filename: str = "inputs/07.dat"):
    log = prepare_simple_input(filename)
    filetree = Filesystem()
    for line in log:
        # AAAAA everything in here is not general enough.
        if line == "$ cd /":
            filetree.current_directory = "/"
        elif line[0] == "$":
            if line[2:4] == "ls":
                continue
            if line[-2:] == "..":
                filetree.cd("..")
            else:  # $ cd <directory>
                filetree.cd(line[5:])
        elif line[0:3] == "dir":
            filetree.add_directory(line[4:])
        else:
            # This is a file. Format:
            # <size> <filename>
            # <size> is a number, <filename> is a string.
            # Filenames don't have spaces in them, and can have any extension or no extension.
            part = line.split(" ")
            filetree.add_file(int(part[0]), part[1])
    return filetree


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


def rig_rock_paper_scissors(prompt: tuple) -> int:
    # Make a name to point relationship. "A" is 1 point, "B" is 2 points, C is 3 points.
    # X is also 1 point, Y is 2 points, Z is 3 points.
    position = {"A": 0, "B": 1, "C": 2}
    winning_outcomes: list[tuple] = [("A", "Y"), ("B", "Z"), ("C", "X")]
    tying_outcomes: list[tuple] = [("A", "X"), ("B", "Y"), ("C", "Z")]
    losing_outcomes: list[tuple] = [("A", "Z"), ("B", "X"), ("C", "Y")]
    # Holy crap those were all autogenerated after typing "winning", "tying", and "losing".
    if prompt[1] == "Z":  # We should win, select that branch.
        outcome = winning_outcomes[position[prompt[0]]]
        return score_rock_paper_scissors(outcome)
    elif prompt[1] == "Y":  # We should tie, select that branch.
        outcome = tying_outcomes[position[prompt[0]]]
        return score_rock_paper_scissors(outcome)
    elif prompt[1] == "X":  # We should lose, select that branch.
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


def find_first_signal_marker(signal: str, marker: str) -> int:
    class SignalMarker(Enum):
        START_OF_PACKET = 4
        START_OF_MESSAGE = 14

    offset = SignalMarker[marker].value
    sig_length = len(signal)
    for i in range(sig_length - offset):
        test_set = set(signal[i : i + offset])
        if len(test_set) == offset:
            return i + offset


def sum_file_sizes(directory):
    sum = 0
    for file_name, value in directory.items():
        if isinstance(value, dict):
            sum += sum_file_sizes(value)
        else:
            sum += value
    return sum


def traverse_sum_sizes(
    directory, max_size, debug=False
):  # TODO: Rename/refactor. 12/18/2022
    total_sizes = 0
    for k, v in directory.items():
        if isinstance(v, dict):
            # v is a dir
            total_sizes += traverse_sum_sizes(v, max_size)
            dir_size = sum_file_sizes(v)
            if debug:
                print(f"Directory {k} has size {dir_size}")
            # if dir is <= input size add to total of sizes
            if dir_size <= max_size:
                total_sizes += dir_size
        else:
            # v is a file
            pass
    if debug:
        print(f"Directory {directory} has size {total_sizes}")
    return total_sizes


def create_list_of_directories(name, filetree, directory_list):
    size_of_dir: int = sum_file_sizes(filetree)
    if name != "":
        directory_list.append((name, size_of_dir))
    else:
        directory_list.append(("/", size_of_dir))
    for k, v in filetree.items():
        if isinstance(v, dict):
            # print(f"Directory: {k}")
            # print(f"Size: {size_of_dir}")
            create_list_of_directories(k, v, directory_list)
    return directory_list


# ====================== Daily Challenges ======================
# More of a scratch place to run each day's challenges. Edit as needed.
if __name__ == "__main__":
    print(day_07b())
