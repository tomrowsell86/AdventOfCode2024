from functools import partial, reduce
from typing import NamedTuple, Tuple


Point = NamedTuple("Point", [("x", "int"), ("y", "int"), ("height", "int")])


def location_delta(a: Point, b: Point):
    return (abs(a.x - b.x), abs(a.y - b.y))


def traverse_graph(location: Point, graph: list[Point]) -> list[Point]:
    if location.height == 9:
        return [location]

    adj_points = [
        p
        for p in graph
        if p.height - location.height == 1
        and (ld := location_delta(location, p))
        and (ld == (1, 0) or ld == (0, 1))
    ]

    return [b for c in (traverse_graph(p, graph) for p in adj_points) for b in c]


def reduce_trailhead_scores(
    part_b: bool, state: Tuple[list[Point], int], trailhead: Point
):
    graph, score = state
    completed_routes = traverse_graph(
        trailhead,
        graph,
    )

    tallest = [t for t in completed_routes if t.height == 9]
    return (graph, score + len(set(tallest) if not part_b else tallest))


with open("input.txt") as file:
    graph = [
        Point(x, y, int(c))
        for y, line in enumerate(file.readlines())
        for x, c in enumerate(line.removesuffix("\n"))
    ]
    trailheads = [p for p in graph if p.height == 0]
    _, part_a_result = reduce(
        partial(reduce_trailhead_scores, False), trailheads, (graph, 0)
    )
    _, part_b_result = reduce(
        partial(reduce_trailhead_scores, True), trailheads, (graph, 0)
    )
    print(part_a_result)
    print(part_b_result)
