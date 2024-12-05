# puzzle prompt: https://adventofcode.com/2023/day/11

import re
from itertools import combinations
from typing import List, Tuple

from ...base import StrSplitSolution, answer


class Grid:
    def __init__(self, lines: List[str]):
        self._rows_to_expand = [
            row for (row, line) in enumerate(lines) if re.match("^\\.+$", line)
        ]

        self._cols_to_expand = [
            col for col in range(len(lines[0])) if all(row[col] == "." for row in lines)
        ]

        self._lines = lines
        self._rows = len(lines)
        self._cols = len(lines[0])

    def galaxies(self):
        for r in range(self._rows):
            for c in range(self._cols):
                if self._lines[r][c] != ".":
                    yield (r, c)

    def distance(self, p1: Tuple[int, int], p2: Tuple[int, int], expansion_size: int):
        """Computes the distance between two points, treating expansion rows and columns to be of the specified size."""
        (r1, c1) = p1
        (r2, c2) = p2

        [ra, rb] = order(r1, r2)
        [ca, cb] = order(c1, c2)

        extra_rows = sum(1 for row in self._rows_to_expand if ra <= row <= rb)
        extra_cols = sum(1 for col in self._cols_to_expand if ca <= col <= cb)

        return abs(r1 - r2) + abs(c1 - c2) + (extra_rows + extra_cols) * expansion_size


def order(i1: int, i2: int):
    return [i1, i2] if i1 <= i2 else [i2, i1]


class Solution(StrSplitSolution):
    _year = 2023
    _day = 11

    @answer(9445168)
    def part_1(self) -> int:
        grid = Grid(self.input)
        galaxies = list(grid.galaxies())

        return sum(grid.distance(g1, g2, 1) for (g1, g2) in combinations(galaxies, 2))

    @answer(742305960572)
    def part_2(self) -> int:
        grid = Grid(self.input)
        galaxies = list(grid.galaxies())

        return sum(
            grid.distance(g1, g2, 999999) for (g1, g2) in combinations(galaxies, 2)
        )
