# puzzle prompt: https://adventofcode.com/2023/day/2

import re
from typing import List

from ...base import StrSplitSolution, answer


class Draw:
    """Represents a draw from the bag, containing some number of each cubes"""

    _counts: dict[str, int]

    def __init__(self):
        self._counts = {}

    def get_count(self, color: str) -> int:
        return self._counts.get(color, 0)

    def set_count(self, color: str, count: int):
        self._counts[color] = count


class Game:
    id: int
    draws: List[Draw]

    def __init__(self, game_number: int, draws: List[Draw]):
        self.id = game_number
        self.draws = draws

    def min_count(self, color: str) -> int:
        return max(draw.get_count(color) for draw in self.draws)

    def power(self) -> int:
        return self.min_count("red") * self.min_count("green") * self.min_count("blue")


def parse_draw(draw: str) -> Draw:
    """Parses a value such as '3 green' or '2 blue, 1 red, 3 green'"""
    bits = draw.split(", ")
    result = Draw()
    for bit in bits:
        [count_str, color] = bit.split()
        count = int(count_str)
        result.set_count(color, count)
    return result


line_regex = re.compile("Game (\\d+): (.*)")


def parse_line(line: str) -> Game:
    # Game 5: 3 green; 2 blue, 1 red, 2 green
    match = line_regex.match(line)
    assert match
    game_num_str, draws_details = match.groups()
    draw_strs = draws_details.split("; ")
    draws = [parse_draw(draw_str) for draw_str in draw_strs]

    return Game(int(game_num_str), draws)


class Solution(StrSplitSolution):
    _year = 2023
    _day = 2

    @answer(2439)
    def part_1(self) -> int:
        all_games = [parse_line(line) for line in self.input]
        possible_games = (
            game
            for game in all_games
            if game.min_count("red") <= 12
            and game.min_count("green") <= 13
            and game.min_count("blue") <= 14
        )
        return sum((game.id for game in possible_games))

    @answer(63711)
    def part_2(self) -> int:
        games = [parse_line(line) for line in self.input]
        return sum(game.power() for game in games)

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
