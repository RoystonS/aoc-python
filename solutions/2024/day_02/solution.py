# puzzle prompt: https://adventofcode.com/2024/day/2

from itertools import pairwise
from typing import List

from ...base import StrSplitSolution, answer


class Solution(StrSplitSolution):
    _year = 2024
    _day = 2

    @answer(534)
    def part_1(self) -> int:
        reports = [parse_report(line) for line in self.input]
        return sum(1 if is_safe(report) else 0 for report in reports)

    @answer(577)
    def part_2(self) -> int:
        reports = [parse_report(line) for line in self.input]
        return sum(
            1 if is_safe(report) or can_be_made_safe(report) else 0
            for report in reports
        )


def is_safe(levels: List[int]) -> bool:
    diffs = [a - b for (a, b) in pairwise(levels)]
    diffs_are_correctly_sized = all(1 <= abs(diff) <= 3 for diff in diffs)

    direction = sign(diffs[0])
    is_monotonic = all(sign(diff) == direction for diff in diffs)

    return diffs_are_correctly_sized and is_monotonic


def can_be_made_safe(levels: List[int]) -> bool:
    for i in range(len(levels)):
        modified_levels = levels.copy()
        del modified_levels[i]
        if is_safe(modified_levels):
            return True
    return False


def parse_report(line: str) -> List[int]:
    # """Parses '1 2 3 4' into [1,2,3,4]"""
    return [int(segment) for segment in line.split()]


def sign(num: int):
    return -1 if num < 0 else 1
