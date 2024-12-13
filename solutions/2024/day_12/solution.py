# puzzle prompt: https://adventofcode.com/2024/day/12

from collections import defaultdict
from typing import Dict, Iterable, Set, Tuple

from ...base import StrSplitSolution, answer
from ...utils.grid import Grid, Position


def apply_grouping(grid: Grid[str], acc: Dict[Position, int]):
    group_id = 0

    for pos in grid.positions():
        if pos not in acc:
            acc[pos] = group_id
            group_letter = grid[pos]
            accumulate_grouping(grid, acc, pos, group_letter, group_id)
            group_id += 1


def accumulate_grouping(
    grid: Grid[str],
    acc: Dict[Position, int],
    pos: Position,
    group_letter: str,
    group_id: int,
):
    for pos in grid.legal_neighbouring_positions_with_value(pos, group_letter):
        if pos not in acc:
            acc[pos] = group_id
            accumulate_grouping(grid, acc, pos, group_letter, group_id)


def collect_groups(groups: Dict[Position, int]) -> Dict[int, Set[Position]]:
    result = defaultdict(set)

    for k, v in groups.items():
        result[v].add(k)

    return result


class Solution(StrSplitSolution):
    _year = 2024
    _day = 12

    @answer(1549354)
    def part_1(self) -> int:
        grid = Grid[str](self.input)
        acc: Dict[Position, int] = {}
        apply_grouping(grid, acc)
        positions_for_groups = collect_groups(acc)

        def perimeters_around(pos: Position, group_letter: str):
            neighbours_of_group = len(
                list(grid.legal_neighbouring_positions_with_value(pos, group_letter))
            )
            return 4 - neighbours_of_group

        def region_price(positions_in_region: Iterable[Position]) -> int:
            positions_list = list(positions_in_region)
            ch = grid[positions_list[0]]

            perimeter_size = sum(perimeters_around(pos, ch) for pos in positions_list)
            area = len(positions_list)

            return perimeter_size * area

        return sum(
            region_price(positions_in_region)
            for positions_in_region in positions_for_groups.values()
        )

    @answer(937032)
    def part_2(self) -> int:
        grid = Grid[str](self.input)
        acc: Dict[Position, int] = {}
        apply_grouping(grid, acc)
        positions_for_groups = collect_groups(acc)

        return sum(
            all_edges(positions) * len(positions)
            for positions in positions_for_groups.values()
        )


def bounds(region: Iterable[Position]) -> Tuple[Position, Position]:
    row_min = min(row for (row, _) in region)
    row_max = max(row for (row, _) in region)
    col_min = min(col for (_, col) in region)
    col_max = max(col for (_, col) in region)

    return (row_min, col_min), (row_max, col_max)


def transpose(positions: Set[Position]) -> Set[Position]:
    return {(col, row) for (row, col) in positions}


def north_south_edges(positions: Set[Position]):
    (row_min, col_min), (row_max, col_max) = bounds(positions)

    total_edge_count = 0

    for row in range(row_min, row_max + 1):

        def check_ns_edge(row_delta: int):
            edge_count = 0

            in_edge = False

            for col in range(col_min, col_max + 1):
                pos = (row, col)
                edge_pos = (row + row_delta, col)

                if pos in positions:
                    if edge_pos not in positions:
                        # We're on an edge
                        if not in_edge:
                            in_edge = True
                            edge_count += 1
                    else:
                        in_edge = False

                else:
                    in_edge = False
            return edge_count

        # Check edges to north and south
        total_edge_count += check_ns_edge(-1)
        total_edge_count += check_ns_edge(+1)

    return total_edge_count


def all_edges(positions: Set[Position]):
    # Count up the edges to the north and south, and then transpose
    # all the positions and do it again, to give us east and west
    return north_south_edges(positions) + north_south_edges(transpose(positions))
