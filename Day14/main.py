import re
from dataclasses import dataclass
from typing import NamedTuple
from math import floor
from functools import reduce

Vector = NamedTuple("Vector", [("x", int), ("y", int)])


@dataclass
class GuardProperty:
    bounds = Vector(101, 103)

    def __init__(
        self,
        origin: Vector,
        velocity: Vector,
    ) -> None:
        self.position = origin
        self.velocity = velocity

    def __repr__(self) -> str:
        return f"p:{self.position}\n"

    def wrap_around(self, product, bounds):
        if product < 0:
            return bounds - abs(product)
        elif product >= bounds:
            return product - bounds
        return product

    def product(self, v1: Vector, v2: Vector):
        nx = self.wrap_around(v1.x + v2.x, self.bounds.x)
        ny = self.wrap_around(v1.y + v2.y, self.bounds.y)
        return Vector(nx, ny)

    def move(self, times: int):
        for _ in range(0, times):
            self.position = self.product(self.position, self.velocity)
            print(self.position)


def parse_guard(line: str):
    regex = re.compile(r"^p=(?P<ox>\d+),(?P<oy>\d+) v=(?P<vx>-?\d+),(?P<vy>-?\d+)$")
    match = regex.search(line)
    if match:
        gd = match.groupdict()
        return GuardProperty(
            Vector(int(gd["ox"]), int(gd["oy"])), Vector(int(gd["vx"]), int(gd["vy"]))
        )
    raise Exception("Could not parse line!")


with open("input.txt") as file:
    guards = [parse_guard(line.removesuffix("\n")) for line in file.readlines()]
    for guard in guards:
        guard.move(100)
    middle_y = floor(103 / 2)
    middle_x = floor(101 / 2)

    def quadrant_reducer(
        state: dict[str, int], current: GuardProperty
    ) -> dict[str, int]:
        def update_state(key, state):
            current_count = state.setdefault(key, 0)
            state[key] = current_count + 1

        match (current.position.x < middle_x, current.position.y < middle_y):
            case (True, True):
                update_state("UL", state)
            case (True, False):
                update_state("LL", state)
            case (False, True):
                update_state("LR", state)
            case (False, False):
                update_state("UR", state)
        return state

    middle_excluded_guards = [
        g for g in guards if g.position.x != middle_x and g.position.y != middle_y
    ]
    quad_counts = reduce(quadrant_reducer, middle_excluded_guards, {})

    result = reduce(lambda prev, curr: prev * curr, quad_counts.values())

    print(result)
