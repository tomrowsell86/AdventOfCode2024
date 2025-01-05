from functools import reduce
import itertools
from typing import DefaultDict, NamedTuple, Tuple


Point = NamedTuple("Point", [("x", "int"), ("y", "int"), ("height", "int")])


with open("input.txt") as file:
    graph = [
        Point(x, y, int(c))
        for y, line in enumerate(file.readlines())
        for x, c in enumerate(line.removesuffix("\n"))
    ]
