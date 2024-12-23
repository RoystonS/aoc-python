# puzzle prompt: https://adventofcode.com/2024/day/22

from itertools import islice, pairwise
from typing import Dict, List, Set, Tuple

from ...base import StrSplitSolution, answer


class Solution(StrSplitSolution):
    _year = 2024
    _day = 22

    @answer((13584398738, 1612))
    def solve(self) -> tuple[int, int]:
        # Compute the lists of secrets once for both parts
        secret_lists = [
            list(islice(run_evolve(int(line)), 0, 2001)) for line in self.input
        ]

        part1 = sum(secret_list[2000] for secret_list in secret_lists)

        unique_keys: Set[int] = set()
        dicts = [
            collect_diffs(secret_list, unique_keys) for secret_list in secret_lists
        ]

        def total(key: Tuple[int, int, int, int]) -> int:
            best_prices = [d.get(key, 0) for d in dicts]
            return sum(best_prices)

        best_prices = (total(key) for key in unique_keys)
        part2 = max(best_prices)

        return (part1, part2)


def collect_diffs(secret_list: List[int], unique_keys: Set[int]) -> Dict[int, int]:
    values = [value % 10 for value in secret_list]
    diffs = [y - x for (x, y) in pairwise(values)]

    first_values: Dict[int, int] = {}

    for i in range(len(diffs) - 3):
        key = 0
        key = tuple(diffs[i : i + 4])

        if key not in first_values:
            # First time we've seen this sequence of diffs for this list
            first_values[key] = values[i + 4]
            unique_keys.add(key)

    return first_values


def run_evolve(num: int):
    while True:
        yield num
        num = evolve(num)


def evolve(secret: int) -> int:
    res = secret * 64
    res = mix(res, secret)
    res = prune(res)
    res2 = res // 32
    res = mix(res, res2)
    res = prune(res)
    res3 = res * 2048
    res = mix(res, res3)
    return prune(res)


def mix(val1: int, val2: int) -> int:
    return val1 ^ val2


def prune(val: int) -> int:
    return val % 16777216
