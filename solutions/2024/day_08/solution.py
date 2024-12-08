# puzzle prompt: https://adventofcode.com/2024/day/8

from collections import defaultdict
from itertools import combinations
from typing import Dict, List, Set, Tuple

from ...base import StrSplitSolution, answer

type Frequency = str
type Position = Tuple[int, int]


class Solution(StrSplitSolution):
    _year = 2024
    _day = 8

    def parse(self):
        d: Dict[Frequency, List[Position]] = defaultdict(list)

        for row_number, line in enumerate(self.input):
            for col_number, ch in enumerate(line):
                if ch != ".":
                    pos = (row_number, col_number)
                    d[ch].append(pos)
        return d

    @answer(354)
    def part_1(self) -> int:
        return self.compute(1, 1)

    @answer(1263)
    def part_2(self) -> int:
        return self.compute(0, 100000)

    def compute(self, min_mult: int, max_mult: int):
        height = len(self.input)
        width = len(self.input[0])

        def in_range(pos: Position) -> bool:
            (r, c) = pos
            return r >= 0 and c >= 0 and r < height and c < width

        antinode_positions: Set[Position] = set()

        frequencies_to_positions = self.parse()

        for positions in frequencies_to_positions.values():
            for [pos1, pos2] in combinations(positions, 2):
                p1r, p1c = pos1
                p2r, p2c = pos2
                dr = p2r - p1r
                dc = p2c - p1c

                mult = min_mult
                while mult <= max_mult:
                    antinode1 = (p1r - dr * mult, p1c - dc * mult)
                    if in_range(antinode1):
                        antinode_positions.add(antinode1)
                        mult += 1
                    else:
                        break

                mult = min_mult
                while mult <= max_mult:
                    antinode2 = (p2r + dr * mult, p2c + dc * mult)
                    if in_range(antinode2):
                        antinode_positions.add(antinode2)
                        mult += 1
                    else:
                        break

        return len(antinode_positions)
