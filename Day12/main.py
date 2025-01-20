from collections.abc import Iterable
from typing import Tuple, NamedTuple
from functools import reduce

Point = NamedTuple("Point", [("x", int), ("y", int)])


class RegionSummary:
    def __init__(self, plant, area, perimeter) -> None:
        self.plant = plant
        self.area = area
        self.perimeter = perimeter

    def __repr__(self) -> str:
        return (
            f"plant : {self.plant}\narea : {self.area} \nperimeter : {self.perimeter}\n"
        )


class RegionScanState:
    def __init__(
        self,
        previous_line: list[Tuple[Point, str]],
        region_buffer: dict[Point, RegionSummary],
        y: int,
    ) -> None:
        self.previous_line = previous_line
        self.region_buffer = region_buffer
        self.y = y

    def __repr__(self) -> str:
        return (
            f"previous_line:{self.previous_line}\nregion_buffer:{self.region_buffer}\n"
        )


def line_gen(file):
    while line := file.readline():
        yield list(line.removesuffix("\n"))


def line_reducer(state: RegionScanState, line: Iterable[str]):
    last_char = None
    prev_line = []

    for x, c in enumerate(line):
        region_key = Point(x, state.y)
        if state.y == 0:
            if last_char and last_char[1] == c:
                region_key = last_char[0]
                region = state.region_buffer[last_char[0]]
                region.perimeter += 1
                region.area += 1
            else:
                if last_char:
                    region = state.region_buffer[last_char[0]]
                    region.perimeter += 1

                state.region_buffer[region_key] = RegionSummary(c, 1, 2)
        elif state.previous_line[x][1] != c and (
            (last_char and last_char[1] != c) or not last_char
        ):
            state.region_buffer[state.previous_line[x][0]].perimeter += 1
            if last_char:
                state.region_buffer[last_char[0]].perimeter += 1
            state.region_buffer[region_key] = RegionSummary(c, 1, 2)
        else:
            if state.previous_line[x][1] == c:
                rs = state.region_buffer[state.previous_line[x][0]]
                region_key = state.previous_line[x][0]
                rs.area += 1
                if not last_char or last_char[1] != c:
                    if last_char:
                        last_r = state.region_buffer[last_char[0]]
                        last_r.perimeter += 1
                    rs.perimeter += 1
                elif (
                    last_char
                    and last_char[1] == c
                    and last_char[0] != state.previous_line[x][0]
                ):
                    merge_source = state.region_buffer[last_char[0]]
                    for i in [
                        i for i, (key, _) in enumerate(prev_line) if key == last_char[0]
                    ]:
                        prev_line[i] = (region_key, c)

                    rs.perimeter += merge_source.perimeter
                    rs.area += merge_source.area
                    state.region_buffer.pop(last_char[0])
            else:
                prev_line_region = state.region_buffer[state.previous_line[x][0]]
                prev_line_region.perimeter += 1
                rs = state.region_buffer[last_char[0]]
                rs.area += 1
                rs.perimeter += 1
                region_key = last_char[0]

        prev_line.append((region_key, c))
        last_char = (region_key, c)

    [last, *_] = reversed(prev_line)
    state.region_buffer[last[0]].perimeter += 1
    return RegionScanState(prev_line, state.region_buffer, state.y + 1)


with open("input.txt") as file:
    gen = line_gen(file)
    reduced_state = reduce(
        line_reducer, [line for line in line_gen(file)], RegionScanState([], {}, 0)
    )
    last_line_regions = [
        reduced_state.region_buffer[a[0]] for a in reduced_state.previous_line
    ]
    for region in last_line_regions:
        region.perimeter += 1
    print(reduced_state)
    result = sum([a.perimeter * a.area for a in reduced_state.region_buffer.values()])
    print(result)
