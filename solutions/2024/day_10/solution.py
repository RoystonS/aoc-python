# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2024/day/10

from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Dict, List, Set, Tuple

from ...base import StrSplitSolution, answer

# We note the positions of each type of value, i.e. all of the 9s, all of the 8s, etc.
# We start with all the 9s, and add those to the list of achievable 9s to all neighbouring 8s.
# We pass those on to all neighbouring 7s, and so on.
# For part 2, it's similar, but we just count the number of paths to 9s

type Position = Tuple[int, int]


DIRECTIONS: List[Position] = [(-1, 0), (0, 1), (1, 0), (0, -1)]


class TopoMap:
    def __init__(self, lines: List[str]):
        self.values = [[int(ch) for ch in line] for line in lines]
        self.height = len(lines)
        self.width = len(lines[0])

    def positions(self):
        return ((row, col) for row in range(self.height) for col in range(self.width))

    def nine_positions(self):
        return (pos for pos in self.positions() if self.get(pos) == 9)

    def get(self, pos: Position):
        row, col = pos
        return self.values[row][col]

    def _all_neighbouring_positions(self, pos: Position):
        row, col = pos
        return [(row + dr, col + dc) for (dr, dc) in DIRECTIONS]

    def is_legal_position(self, pos: Position):
        row, col = pos
        return row >= 0 and col >= 0 and row < self.height and col < self.width

    def legal_neighbouring_positions(self, pos: Position):
        return (
            p
            for p in self._all_neighbouring_positions(pos)
            if self.is_legal_position(p)
        )

    def legal_neighbouring_positions_with_value(self, pos: Position, value: int):
        return [
            p for p in self.legal_neighbouring_positions(pos) if self.get(p) == value
        ]


class Solution(StrSplitSolution):
    _year = 2024
    _day = 10

    @answer(617)
    def part_1(self) -> int:
        m = TopoMap(self.input)
        store = Store1()
        traverse(m, store)

        return sum(
            len(store.get_nines_available_from(pos))
            for pos in m.positions()
            if m.get(pos) == 0
        )

    @answer(1477)
    def part_2(self) -> int:
        m = TopoMap(self.input)
        store = Store2()
        traverse(m, store)

        return sum(
            store.get_nines_available_from(pos)
            for pos in m.positions()
            if m.get(pos) == 0
        )


class Store(ABC):
    @abstractmethod
    def add_nine(self, pos: Position):
        pass

    @abstractmethod
    def merge_nines(self, src: Position, dest: Position):
        pass


class Store1(Store):
    def __init__(self):
        self.nines_available_from: Dict[Position, Set[Position]] = defaultdict(set)

    def add_nine(self, pos: Position):
        self.nines_available_from[pos].add(pos)

    def merge_nines(self, src: Position, dest: Position):
        for nine_from_pos in self.nines_available_from[src]:
            self.nines_available_from[dest].add(nine_from_pos)

    def get_nines_available_from(self, pos: Position):
        return self.nines_available_from[pos]


class Store2(Store):
    def __init__(self):
        self.nines_available_from: Dict[Position, int] = defaultdict(lambda: 0)

    def add_nine(self, pos: Position):
        self.nines_available_from[pos] = 1

    def merge_nines(self, src: Position, dest: Position):
        self.nines_available_from[dest] += self.nines_available_from[src]

    def get_nines_available_from(self, pos: Position):
        return self.nines_available_from[pos]


def traverse(m: TopoMap, store: Store):
    all_nine_positions = list(m.nine_positions())

    for pos in all_nine_positions:
        store.add_nine(pos)

    previous_level_positions = all_nine_positions
    next_level_positions: Set[Position] = set()
    level = 9

    while level > 0:
        for pos in previous_level_positions:
            next_level = level - 1
            for p2 in m.legal_neighbouring_positions_with_value(pos, next_level):
                next_level_positions.add(p2)
                store.merge_nines(pos, p2)
        previous_level_positions = next_level_positions
        level = next_level
        next_level_positions = set()
