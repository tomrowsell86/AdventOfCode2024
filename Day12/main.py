from collections.abc import Iterable
from typing import Tuple
from functools import reduce


class RegionSummary:
    def __init__(self, region_id, plant, area, perimeter) -> None:
        self.region_id = region_id
        self.plant = plant
        self.area = area
        self.perimeter = perimeter


class RegionScanState:
    def __init__(
        self,
        previous_line: Iterable[str],
        completed_regions: list[RegionSummary],
        region_buffer: dict[Tuple[int, int], RegionSummary],
    ) -> None:
        self.previous_line = previous_line
        self.completed_regions = completed_regions
        self.__next_id = 0

    def get_next_id(self):
        self.__next_id += 1
        return self.__next_id


def line_gen(file):
    while line := file.readline():
        yield list(line)


def line_reducer(state: RegionScanState, line: Iterable[str]):
    return state


with open("input.txt") as file:
    gen = line_gen(file)
    fst = gen.send(None)
    reduced_state = reduce(
        line_reducer, [line for line in line_gen(file)], RegionScanState(fst[1], [], {})
    )
    result = sum([a.perimeter * a.area for a in reduced_state.completed_regions])
    print(result)
