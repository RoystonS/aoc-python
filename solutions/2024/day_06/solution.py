# puzzle prompt: https://adventofcode.com/2024/day/6

from concurrent.futures import ProcessPoolExecutor
from enum import Enum
from typing import Dict, List, Tuple

from ...base import StrSplitSolution, answer

type Position = Tuple[int, int]

DIRECTIONS: List[Position] = [(-1, 0), (0, 1), (1, 0), (0, -1)]


# The state of a guard
class GuardState(Enum):
    FREELY_MOVING = 1
    EXITED_MAZE = 2
    DETECTED_LOOP = 3


class Maze:
    def __init__(self, lines: List[str]):
        self.lines = lines
        self.height = len(lines)
        self.width = len(lines[0])


class Guard:
    def __init__(self, maze: Maze, obstruction_pos: Position | None = None):
        self.maze = maze
        self.dir = 0
        self.state = GuardState.FREELY_MOVING
        self.obstruction_pos = obstruction_pos

        self.row = [
            index for (index, line) in enumerate(maze.lines) if line.find("^") >= 0
        ][0]
        self.col = maze.lines[self.row].find("^")

        self.visited_count: Dict[Position, int] = {}
        self.visited_count[(self.row, self.col)] = 1

    def next_position(self) -> Position | None:
        (delta_row, delta_col) = DIRECTIONS[self.dir]
        next_row = self.row + delta_row
        next_col = self.col + delta_col

        if next_row < 0 or next_col < 0:
            return None
        if next_row >= self.maze.height or next_col >= self.maze.width:
            return None
        return (next_row, next_col)

    def move(self):
        next_pos = self.next_position()
        if next_pos is None:
            self.state = GuardState.EXITED_MAZE
            return

        (next_row, next_col) = next_pos
        item_in_front = self.maze.lines[next_row][next_col]

        if item_in_front == "#" or next_pos == self.obstruction_pos:
            # Blocked, so turn and try again
            self.dir = (self.dir + 1) % len(DIRECTIONS)
            self.move()
            return

        self.row = next_row
        self.col = next_col
        new_count = self.visited_count.get(next_pos, 0) + 1
        self.visited_count[next_pos] = new_count
        if new_count > 4:
            # Cycle
            self.state = GuardState.DETECTED_LOOP

    def move_until_exit(self):
        while self.state == GuardState.FREELY_MOVING:
            self.move()


def guard_loops(guard: Guard):
    guard.move_until_exit()
    return 1 if guard.state == GuardState.DETECTED_LOOP else 0


class Solution(StrSplitSolution):
    _year = 2024
    _day = 6

    @answer((4826, 1721))
    def solve(self) -> tuple[int, int]:
        maze = Maze(self.input)

        original_guard = Guard(maze)
        original_guard.move_until_exit()

        # Now we've computed the original path, consider turning
        # all of the visited positions into obstructions.
        # (This means we consider about 5000 positions instead of all 17000)
        # We could go even faster by reusing large portions of the path,
        # knowing that the path will be the same up until the first time we hit
        # each position.

        # Create a series of guards with an extra obstruction in place
        guards_with_obstructions = (
            Guard(maze, pos) for pos in original_guard.visited_count
        )

        # And run them in parallel. :-)
        with ProcessPoolExecutor() as executor:
            obstructions_causing_loops = sum(
                executor.map(guard_loops, guards_with_obstructions)
            )

        return len(original_guard.visited_count), obstructions_causing_loops
