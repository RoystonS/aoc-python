# puzzle prompt: https://adventofcode.com/2024/day/14

import re
from collections import Counter
from typing import Iterable, Tuple

from ...base import StrSplitSolution, answer, slow

type Vector = Tuple[int, int]
type Position = Vector
type Velocity = Vector

# p=18,21 v=31,52
pattern = re.compile("p=(-?\\d+),(-?\\d+) v=(-?\\d+),(-?\\d+)")


def parse_line(line: str) -> Tuple[Vector, Vector]:
    match = pattern.match(line)
    return [
        [int(match.group(1)), int(match.group(2))],
        [int(match.group(3)), int(match.group(4))],
    ]


class Solution(StrSplitSolution):
    _year = 2024
    _day = 14

    def get_width_height(self) -> Tuple[int, int]:
        if len(self.input) > 20:
            return (101, 103)
        return (11, 7)

    @answer(231221760)
    def part_1(self) -> int:
        width, height = self.get_width_height()

        mid_row = (height - 1) // 2
        mid_col = (width - 1) // 2

        robots = [parse_line(line) for line in self.input]
        final_positions = [advance(robot, 100, width, height) for robot in robots]
        final_quadrants = [
            determine_quadrant(final_position, mid_row, mid_col)
            for final_position in final_positions
        ]
        counts = Counter(final_quadrants)
        return counts[0] * counts[1] * counts[2] * counts[3]

    @answer(6771)
    @slow
    def part_2(self) -> int:
        robots = [parse_line(line) for line in self.input]
        width, height = self.get_width_height()

        steps = 0

        positions = [pos for (pos, _) in robots]

        def calc_pos(latest_pos: Position, velocity: Velocity) -> Position:
            (x, y) = latest_pos
            (dx, dy) = velocity
            return ((x + dx) % width, (y + dy) % height)

        while True:
            x_count = Counter(x for (x, y) in positions)
            max_x_count = max(count for count in x_count.values())
            y_count = Counter(y for (x, y) in positions)
            max_y_count = max(count for count in y_count.values())

            # How do we detect a 'tree'? We look for any layout that has
            # at least 32 in one row and column
            if max_x_count >= 32 and max_y_count >= 32:
                # print_positions(positions, width, height)
                return steps

            steps += 1
            new_positions = [
                calc_pos(latest_pos, robots[i][1])
                for (i, latest_pos) in enumerate(positions)
            ]

            positions = new_positions


def print_positions(positions: Iterable[Position], width: int, height: int):
    pic = {}
    for pos in positions:
        prev = pic.get(pos, "0")
        pic[(pos)] = str(int(prev) + 1)
    for y in range(height):
        for x in range(width):
            print(pic.get((x, y), "."), end="")
        print()
    print()


def advance(
    start: Tuple[Position, Velocity], steps: int, width: int, height: int
) -> Position:
    (start_pos, vel) = start
    (start_x, start_y) = start_pos
    (dx, dy) = vel

    final_x = (start_x + steps * dx) % width
    final_y = (start_y + steps * dy) % height

    return (final_x, final_y)


def determine_quadrant(pos: Position, mid_row: int, mid_col: int) -> int:
    (x, y) = pos

    if y < mid_row:
        if x < mid_col:
            return 0
        if x > mid_col:
            return 1
    elif y > mid_row:
        if x < mid_col:
            return 2
        if x > mid_col:
            return 3

    return None
