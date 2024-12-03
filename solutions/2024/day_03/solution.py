# puzzle prompt: https://adventofcode.com/2024/day/3

import re
from abc import ABC, abstractmethod
from functools import reduce
from typing import Iterable, List, Tuple

from ...base import TextSolution, answer

type State = Tuple[int, bool]


class Instruction(ABC):
    @abstractmethod
    def execute(self, state: State) -> State:
        pass


class MulInstruction(Instruction):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def execute(self, state: State):
        (value, enabled) = state

        return state if not enabled else (value + self.x * self.y, enabled)


class EnablementInstruction(Instruction):
    def __init__(self, enabled: bool):
        self.enabled = enabled

    def execute(self, state: State):
        (value, _enabled) = state
        return (value, self.enabled)


class Solution(TextSolution):
    _year = 2024
    _day = 3

    def get_instructions(self) -> List[Instruction]:
        instruction_texts = re.findall(
            "((?:mul\\(\\d+,\\d+\\))|(?:don't\\(\\))|(?:do\\(\\)))", self.input
        )
        result: List[Instruction] = []
        for text in instruction_texts:
            if text == "don't()":
                result.append(EnablementInstruction(False))
            elif text == "do()":
                result.append(EnablementInstruction(True))
            else:
                match = re.match("mul\\((\\d+),(\\d+)\\)", text)
                assert match
                [x, y] = match.groups()
                result.append(MulInstruction(int(x), int(y)))
        return result

    @answer(173785482)
    def part_1(self) -> int:
        all_instructions = self.get_instructions()
        filtered_instructions = (
            instr for instr in all_instructions if isinstance(instr, MulInstruction)
        )
        (value, _enabled) = run_instructions(filtered_instructions)
        return value

    @answer(83158140)
    def part_2(self) -> int:
        instructions = self.get_instructions()
        (value, _enabled) = run_instructions(instructions)
        return value


def run_instructions(instructions: Iterable[Instruction]):
    initial_state: State = (0, True)
    return reduce(lambda state, i: i.execute(state), instructions, initial_state)
