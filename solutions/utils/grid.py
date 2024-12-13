from typing import Generic, List, Tuple, TypeVar

type Position = Tuple[int, int]

T = TypeVar("T")

DIRECTIONS: List[Position] = [(-1, 0), (0, 1), (1, 0), (0, -1)]


class Grid(Generic[T]):
    def __init__(self, lines: List[List[T]]):
        self.values = lines
        self.height = len(lines)
        self.width = len(lines[0])

    def positions(self):
        return ((row, col) for row in range(self.height) for col in range(self.width))

    def __getitem__(self, pos: Position) -> T:
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

    def legal_neighbouring_positions_with_value(self, pos: Position, value: T):
        return [p for p in self.legal_neighbouring_positions(pos) if self[p] == value]
