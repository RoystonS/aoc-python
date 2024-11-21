# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/1

from ...base import StrSplitSolution, answer

NUMBERS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


class Solution(StrSplitSolution):
    _year = 2023
    _day = 1

    @answer(54953)
    def part_1(self) -> int:
        return sum(compute_calibration(line) for line in self.input)

    @answer(53868)
    def part_2(self) -> int:
        return sum(compute_calibration(replace_words(line)) for line in self.input)


def replace_words(s: str) -> str:
    # We should keep the first and last letter of each replaced word to cope
    # with overlaps with other words.
    # eightwothree -> eight2othree -> eight2ot3e -> e8t2ot3e
    for num, digit in NUMBERS.items():
        s = s.replace(num, f"{num[0]}{digit}{num[-1]}")
    return s


def compute_calibration(s: str) -> int:
    digits = [c for c in s if c.isdigit()]
    assert digits, f"No digits in {s}"
    return int(digits[0] + digits[-1])
