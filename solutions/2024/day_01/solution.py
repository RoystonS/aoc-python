# puzzle prompt: https://adventofcode.com/2024/day/1

from collections import Counter

from ...base import StrSplitSolution, answer


class Solution(StrSplitSolution):
    _year = 2024
    _day = 1

    def input_tuples(self):
        split_lines = (line.split() for line in self.input)
        return [(int(line[0]), int(line[1])) for line in split_lines]

    def input_lists(self):
        input_tuples = self.input_tuples()
        first_list = [n1 for (n1, n2) in input_tuples]
        second_list = [n2 for (n1, n2) in input_tuples]
        return (first_list, second_list)

    @answer(1320851)
    def part_1(self) -> int:
        (first_list, second_list) = self.input_lists()

        first_list.sort()
        second_list.sort()

        differences = (abs(n1 - n2) for (n1, n2) in zip(first_list, second_list))
        return sum(differences)

    @answer(26859182)
    def part_2(self) -> int:
        (first_list, second_list) = self.input_lists()

        second_list_counts = Counter(second_list)
        counts = (item * second_list_counts[item] for item in first_list)
        return sum(counts)
