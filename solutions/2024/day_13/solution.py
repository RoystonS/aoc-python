# puzzle prompt: https://adventofcode.com/2024/day/13
import math
import re
from typing import List

from ...base import StrSplitSolution, answer


class XY:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class ClawMachine:
    def __init__(self, info_a: XY, info_b: XY, prize: XY):
        self.info_a = info_a
        self.info_b = info_b
        self.prize = prize


button_pattern = re.compile("Button [AB]: X([-+\\d]+), Y([-+\\d]+)")
prize_pattern = re.compile("Prize: X=(\\d+), Y=(\\d+)")


def read_button_info(line: str):
    m = button_pattern.match(line)
    return XY(int(m.groups()[0]), int(m.groups()[1]))


def read_prize_info(line: str):
    m = prize_pattern.match(line)
    return XY(int(m.groups()[0]), int(m.groups()[1]))


class Solution(StrSplitSolution):
    _year = 2024
    _day = 13

    def _parse(self) -> List[ClawMachine]:
        line_iterator = iter(self.input)
        claw_machines: List[ClawMachine] = []

        try:
            while True:
                info_a = read_button_info(next(line_iterator))
                info_b = read_button_info(next(line_iterator))
                prize = read_prize_info(next(line_iterator))
                claw = ClawMachine(info_a, info_b, prize)
                claw_machines.append(claw)
                next(line_iterator)
        except StopIteration:
            pass

        return claw_machines

    @answer(32026)
    def part_1(self) -> int:
        claw_machines = self._parse()
        return sum(
            tokens_for_cheapest_option(claw_machine) for claw_machine in claw_machines
        )

    @answer(89013607072065)
    def part_2(self) -> int:
        claw_machines = self._parse()
        for claw_machine in claw_machines:
            claw_machine.prize.x += 10000000000000
            claw_machine.prize.y += 10000000000000
        return sum(
            tokens_for_cheapest_option(claw_machine) for claw_machine in claw_machines
        )


def tokens_for_cheapest_option(claw_machine: ClawMachine):
    press_options2 = list(get_presses(claw_machine))

    if len(press_options2) > 0:
        return min(
            a_presses * 3 + b_presses for (a_presses, b_presses) in press_options2
        )
    return 0


def get_presses(claw_machine: ClawMachine):
    info_a = claw_machine.info_a
    info_b = claw_machine.info_b
    prize = claw_machine.prize

    # We have two equations
    # prize.x = a_presses * info_a.x + b_presses * info_b.x
    # prize.y = a_presses * info_a.y + b_presses * info_b.y

    # We can't use numpy to solve it via linalg.solve because it doesn't provide enough accuracy because
    # of its use of floating point arithmetic. So we have to solve manually.
    # We don't want to do any non-integer division, so we multiply both
    # equations to produce a_presses * lcm(info_a.x and info_a.y) in both equations
    a_lcm = math.lcm(info_a.x, info_a.y)
    factor1 = a_lcm // info_a.x
    factor2 = a_lcm // info_a.y
    # prize.x * factor1 = a_presses * a_lcm + b_presses * info_b.x * factor1
    # prize.y * factor2 = a_presses * a_lcm + b_presses * info_b.y * factor2
    # Rearranging and subtracting `a_presses * a_lcm``, we get
    # prize.x * factor1 - b_presses * info_b.x * factor1 = prize.y * factor2 - b_presses * info_b.y * factor2
    # =>
    # prize.x * factor1 - prize.y * factor2 = b_presses * info_b.x * factor1 - b_presses * info_b.y * factor2
    # =>
    # prize.x * factor1 - prize.y * factor2 = b_presses * (info_b.x * factor1 - info_b.y * factor2)
    # =>
    # (prize.x * factor1 - prize.y * factor2) / (info_b.x * factor1 - info_b.y * factor2) = b_presses
    b_presses = (prize.x * factor1 - prize.y * factor2) // (
        info_b.x * factor1 - info_b.y * factor2
    )
    a_presses = (prize.x - b_presses * info_b.x) // info_a.x

    # We've forced both to use integer arithmetic, to preserve accuracy, so the answers may be wrong. Test.
    if (
        a_presses * info_a.x + b_presses * info_b.x == prize.x
        and a_presses * info_a.y + b_presses * info_b.y == prize.y
    ):
        yield (a_presses, b_presses)
