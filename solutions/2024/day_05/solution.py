# puzzle prompt: https://adventofcode.com/2024/day/5

from graphlib import TopologicalSorter
from typing import Iterable, List, Set, Tuple

from ...base import StrSplitSolution, answer


class Rule:
    def __init__(self, before: int, after: int):
        self.before = before
        self.after = after


class Update:
    def __init__(self, pages: List[int]):
        self.pages = pages

        # Compute the rules which would be problematic for this update
        prohibited_rules: Set[Tuple[int, int]] = set()

        # e.g. for 1,2,3, we can look at 1 and see that (2,1) and (3,1) would be problematic. And then (3,2)
        for index, earlier_page in enumerate(pages):
            for later_page in pages[index + 1 :]:
                prohibited_rules.add((later_page, earlier_page))
        self._prohibited_rules = prohibited_rules

    def satisfies_rules(self, rules: Iterable[Rule]):
        matches = (
            (rule.before, rule.after) not in self._prohibited_rules for rule in rules
        )
        return all(matches)

    def middle_page(self):
        return self.pages[(len(self.pages) - 1) // 2]

    def __repr__(self):
        return f"{self.pages}"


class Solution(StrSplitSolution):
    _year = 2024
    _day = 5

    def parse_input(self):
        rules: List[Rule] = []
        updates: List[Update] = []

        reading_rules = True

        for line in self.input:
            if line == "":
                reading_rules = False
                continue
            if reading_rules:
                [before, after] = [int(segment) for segment in line.split("|")]
                rules.append(Rule(before, after))
            else:
                pages = [int(segment) for segment in line.split(",")]
                updates.append(Update(pages))

        return (rules, updates)

    @answer(5064)
    def part_1(self) -> int:
        (rules, updates) = self.parse_input()

        good_updates = (update for update in updates if update.satisfies_rules(rules))
        middle_pages = (update.middle_page() for update in good_updates)
        return sum(middle_pages)

    @answer(5152)
    def part_2(self) -> int:
        # It would be nice to be able to do a single topological sort across all the rules
        # but unfortunately the rules form a _cyclic_ graph. So we do a tsort of the subset
        # of nodes that actually pertain to each Update.
        (rules, updates) = self.parse_input()

        incorrect_updates = [
            update for update in updates if not update.satisfies_rules(rules)
        ]

        total = 0

        for update in incorrect_updates:
            pages = set(update.pages)
            sorter = TopologicalSorter()
            for rule in rules:
                if rule.before in pages and rule.after in pages:
                    sorter.add(rule.after, rule.before)
            sorted_pages = list(sorter.static_order())
            sorted_update = Update(sorted_pages)
            total += sorted_update.middle_page()

        return total
