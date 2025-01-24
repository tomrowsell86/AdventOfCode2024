from collections.abc import Iterable
from typing import NamedTuple
from functools import reduce
from itertools import pairwise

Point = NamedTuple("Point", [("x", int), ("y", int)])
RegionPair = NamedTuple("RegionPair", [("region_key", Point), ("plot", str)])


class RegionSummary:
    def __init__(self, plant, area, perimeter, sides) -> None:
        self.plant = plant
        self.area = area
        self.perimeter = perimeter
        self.sides = sides

    def __repr__(self) -> str:
        return f"plant : {self.plant}\narea : {self.area} \nperimeter : {self.perimeter}\nsides : {self.sides}\n"


class RegionScanState:
    def __init__(
        self,
        previous_line: list[RegionPair],
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
    for x, plot in enumerate(line):
        region_key = Point(x, state.y)
        if state.y == 0:
            if last_char and last_char.plot == plot:
                region_key = last_char.region_key
                region = state.region_buffer[region_key]
                region.perimeter += 1
                region.area += 1
            else:
                if last_char:
                    region = state.region_buffer[last_char.region_key]
                    region.perimeter += 1
                    region.sides += 1

                state.region_buffer[region_key] = RegionSummary(plot, 1, 2, 2)
        elif state.previous_line[x].plot != plot and (
            (last_char and last_char.plot != plot) or not last_char
        ):
            r = state.region_buffer[state.previous_line[x].region_key]
            r.perimeter += 1
            if last_char:
                l_region = state.region_buffer[last_char.region_key]
                l_region.perimeter += 1
                if (
                    state.previous_line[x].region_key
                    == state.previous_line[x - 1].region_key
                    or state.previous_line[x - 1].region_key != last_char.region_key
                ):
                    l_region.sides += 1

                if (
                    state.previous_line[x - 1].region_key
                    != state.previous_line[x].region_key
                    or state.previous_line[x].region_key == last_char.region_key
                ):
                    r.sides += 1
            else:
                r.sides += 1
            state.region_buffer[region_key] = RegionSummary(plot, 1, 2, 2)
        else:
            if state.previous_line[x].plot == plot:
                region_key = state.previous_line[x].region_key
                rs = state.region_buffer[region_key]
                rs.area += 1
                if not last_char or last_char.plot != plot:
                    if last_char:
                        last_r = state.region_buffer[last_char.region_key]
                        last_r.perimeter += 1
                        if (
                            state.previous_line[x - 1].region_key
                            != last_char.region_key
                        ):
                            last_r.sides += 1
                            if state.previous_line[x - 1].region_key == region_key:
                                rs.sides += 1

                    rs.perimeter += 1
                elif (
                    last_char
                    and last_char.plot == plot
                    and last_char.region_key != state.previous_line[x].region_key
                ):
                    merge_source = state.region_buffer[last_char.region_key]
                    for i in [
                        i
                        for i, (key, _) in enumerate(prev_line)
                        if key == last_char.region_key
                    ]:
                        prev_line[i] = RegionPair(region_key, plot)

                    rs.sides += merge_source.sides
                    rs.perimeter += merge_source.perimeter
                    rs.area += merge_source.area
                    state.region_buffer.pop(last_char.region_key)
            elif last_char:
                prev_line_region = state.region_buffer[
                    state.previous_line[x].region_key
                ]
                prev_line_region.perimeter += 1
                rs = state.region_buffer[last_char.region_key]
                if (
                    state.previous_line[x - 1].region_key
                    != state.previous_line[x].region_key
                ):
                    prev_line_region.sides += 1
                    if state.previous_line[x - 1].region_key == last_char.region_key:
                        rs.sides += 1
                rs.area += 1
                rs.perimeter += 1
                region_key = last_char.region_key

        prev_line.append(RegionPair(region_key, plot))
        last_char = RegionPair(region_key, plot)

    [last, *_] = reversed(prev_line)
    state.region_buffer[last.region_key].perimeter += 1
    if (
        state.y == 0
        or state.previous_line[len(prev_line) - 1].region_key != last.region_key
    ):
        state.region_buffer[last.region_key].sides += 1
    return RegionScanState(prev_line, state.region_buffer, state.y + 1)


with open("input.txt") as file:
    gen = line_gen(file)
    reduced_state = reduce(
        line_reducer, [line for line in line_gen(file)], RegionScanState([], {}, 0)
    )
    last_line_regions = [
        (a[0], reduced_state.region_buffer[a[0]]) for a in reduced_state.previous_line
    ]

    for i, ((fk, fr), (sk, sr)) in enumerate(pairwise(last_line_regions)):
        if i == 0:
            fr.perimeter += 1
            fr.sides += 1

        sr.perimeter += 1
        if sk != fk:
            sr.sides += 1

    result_a = sum([a.perimeter * a.area for a in reduced_state.region_buffer.values()])
    result_b = sum([a.sides * a.area for a in reduced_state.region_buffer.values()])
    print(result_b)
    print(result_a)
