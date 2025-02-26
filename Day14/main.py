import re
from dataclasses import dataclass
from typing import NamedTuple
from math import floor

Vector = NamedTuple("Vector", [("x", int), ("y", int)])


@dataclass
class GuardProperty:
    bounds = Vector(11, 7)

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
    vx = floor(11 / 2)
    vy = floor(7 / 2)
    q1 = [g for g in guards if g.position.x < vx and g.position.y < vy]
    q2 = [g for g in guards if g.position.x > vx and g.position.y < vy]
    q3 = [g for g in guards if g.position.x < vx and g.position.y > vy]
    q4 = [g for g in guards if g.position.x < vx and g.position.y > vy]

    print(min([len(q) for q in [q1, q2, q3, q4]]))

    print(guards)
