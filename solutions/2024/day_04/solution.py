# puzzle prompt: https://adventofcode.com/2024/day/4

from itertools import zip_longest
from typing import Iterable, Tuple

from ...base import StrSplitSolution, answer

DIRECTIONS = [
    (dr, dc) for dr in range(-1, 2) for dc in range(-1, 2) if dr != 0 or dc != 0
]


class Grid:
    def __init__(self, data: list[str]):
        self._data = [list(line) for line in data]
        self.height = len(self._data)
        self.width = len(self._data[0])

    def _out_of_range(self, row: int, col: int) -> bool:
        return row < 0 or col < 0 or row >= self.height or col >= self.width

    def get(self, row: int, col: int) -> str | None:
        if self._out_of_range(row, col):
            return None
        return self._data[row][col]

    def is_xmas(self, pos: Tuple[int, int]) -> bool:
        (row, col) = pos
        if self.get(row, col) == "A":
            tl = self.get(row - 1, col - 1)
            if tl != "M" and tl != "S":
                return False
            if self.get(row + 1, col + 1) != opposite_xmas(tl):
                return False

            tr = self.get(row - 1, col + 1)
            if tr != "M" and tr != "S":
                return False
            return self.get(row + 1, col - 1) == opposite_xmas(tr)
        return False

    def positions(self):
        """Returns all the positions in the grid"""
        for r in range(self.height):
            for c in range(self.width):
                yield (r, c)

    def follow_direction(self, pos: Tuple[int, int], delta: Tuple[int, int]):
        """Returns all the positions available from a point, in a specified direction"""
        (row, col) = pos
        (dr, dc) = delta

        while True:
            yield self.get(row, col)
            row += dr
            col += dc
            if self._out_of_range(row, col):
                return


def opposite_xmas(ch: str):
    return "M" if ch == "S" else "S"


def matches(iter1: Iterable[str], iter2: Iterable[str]) -> bool:
    return all(a == b for (a, b) in zip_longest(iter1, iter2, fillvalue=None))


# TODO: is there not a version of this built into Python?
def take[T](it: Iterable[T], count: int):
    for i in it:
        if count == 0:
            return
        count -= 1
        yield i


class Solution(StrSplitSolution):
    _year = 2024
    _day = 4

    @answer(2507)
    def part_1(self) -> int:
        grid = Grid(self.input)
        search = list("XMAS")
        search_length = len(search)

        return sum(
            1
            for start_pos in grid.positions()
            for direction in DIRECTIONS
            if matches(
                search,
                take(grid.follow_direction(start_pos, direction), search_length),
            )
        )

    @answer(1969)
    def part_2(self) -> int:
        grid = Grid(self.input)
        return sum(1 for position in grid.positions() if grid.is_xmas(position))
