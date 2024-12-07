# puzzle prompt: https://adventofcode.com/2024/day/7

from typing import List, Tuple

from ...base import StrSplitSolution, answer

# Our main observation for this puzzle is that because we're only expecting integers,
# we can rule out multiplication operations if the division result isn't integral.
# e.g. if we have 292: 11 6 16 20, we KNOW that the last operation can't be a multiply
# because no integer muliplied by 20 would give 292.
# This means we process the numbers _backwards_.
# This also makes concatenation-testing trivial.

type Equation = Tuple[int, List[int]]


class Solution(StrSplitSolution):
    _year = 2024
    _day = 7

    def _read_equations(self):
        return [parse_line(line) for line in self.input]

    @answer(303766880536)
    def part_1(self) -> int:
        return self._compute(allow_concatenation=False)

    @answer(337041851384440)
    def part_2(self) -> int:
        return self._compute(allow_concatenation=True)

    def _compute(self, allow_concatenation: bool) -> int:
        return sum(
            total
            for (total, nums) in self._read_equations()
            if has_solutions(total, nums, allow_concatenation=allow_concatenation)
        )


def has_solutions(
    original_total: int, all_nums: List[int], allow_concatenation: bool
) -> bool:
    def inner_test(total: int, nums: List[int]) -> bool:
        if len(nums) == 1:
            return nums[0] == total

        [first, *rest] = nums

        # Can we use multiply?
        (divisor, remainder) = divmod(total, first)
        if remainder == 0 and inner_test(divisor, rest):
            # We have a clean division and the rest of the equation works
            return True

        # Test concatenation
        if allow_concatenation:
            total_str = str(total)
            first_str = str(first)
            first_str_len = len(first_str)
            if (
                total >= 0
                and len(total_str) > first_str_len
                and total_str[-first_str_len:] == first_str
            ):
                # The total ends with this number
                remaining_after_concatenation = total_str[:-first_str_len]
                if inner_test(int(remaining_after_concatenation), rest):
                    # We have a clean concatenation and the rest of the equation works
                    return True

        # Test addition
        remaining_after_addition = total - first
        return inner_test(remaining_after_addition, rest)

    return inner_test(original_total, list(reversed(all_nums)))


def parse_line(line: str) -> Tuple[int, List[int]]:
    [total_str, rest_str] = line.split(": ")
    return (int(total_str), [int(num) for num in rest_str.split()])
