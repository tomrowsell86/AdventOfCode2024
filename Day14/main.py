import dataclasses
from os import posix_fallocate
import re
from dataclasses import dataclass
from typing import NamedTuple

Vector = NamedTuple("Vector", [("x", int), ("y", int)])


@dataclass
class GuardProperty:
    def __init__(
        self,
        origin: Vector,
        velocity: Vector,
    ) -> None:
        self.position = origin
        self.velocity = velocity

    def __repr__(self) -> str:
        return f"p:{self.position},v:{self.velocity}"

    def product(self, v1: Vector, v2: Vector):
        return Vector(v1.x + v2.x, v1.y + v2.y)

    def move(self, times: int):
        for _ in range(1, times):
            self.position = self.product(self.position, self.velocity)


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
    print(guards)
