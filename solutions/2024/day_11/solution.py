# puzzle prompt: https://adventofcode.com/2024/day/11

# The trick for this day is not to try to keep hold of the list of stones, but just to compute the
# number of stones each stone morphs into, and to apply memoization. The cache ends up with 116314 entries in it.

from typing import Dict, Tuple

from ...base import IntSplitSolution, answer

cache: Dict[Tuple[int, int], int] = {}


def blink(stone: int, levels: int) -> int:
    if levels == 0:
        return 1

    cache_key = (stone, levels)
    result = cache.get(cache_key)
    if result is not None:
        return result

    if stone == 0:
        result = blink(1, levels - 1)
    else:
        stone_str = str(stone)
        if len(stone_str) % 2 == 0:
            midpoint = len(stone_str) // 2
            new_stone_1 = int(stone_str[:midpoint])
            new_stone_2 = int(stone_str[midpoint:])

            result = blink(new_stone_1, levels - 1) + blink(new_stone_2, levels - 1)
        else:
            result = blink(stone * 2024, levels - 1)

    cache[cache_key] = result
    return result


class Solution(IntSplitSolution):
    _year = 2024
    _day = 11
    separator = " "

    @answer(222461)
    def part_1(self) -> int:
        return sum(blink(stone, 25) for stone in self.input)

    @answer(264350935776416)
    def part_2(self) -> int:
        return sum(blink(stone, 75) for stone in self.input)
