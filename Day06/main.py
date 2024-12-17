from typing import Tuple
from itertools import accumulate

directionSet = set(["<", ">", "^", "v"])


class Point:
    x: int
    y: int


def parseLine(linePlusIndex: Tuple[int, str]):
    y, line = linePlusIndex
    return list(
        map(
            lambda ic: (ic[0], y, ic[1]),
            filter(
                lambda ic: ic[1] == "#" or ic[1] in directionSet,
                enumerate(list(line.removesuffix("\n"))),
            ),
        )
    )


def tracePath(position: Tuple[int, int], obstacles: list[Tuple[int, int]]):
    x, y = position
    return any([(ox, oy) for ox, oy in obstacles if ox == x and oy == y])


def moveGuard(
    guardPosition: Tuple[int, int, str],
    obstacles: list[Tuple[int, int]],
    visited: set[Tuple[int, int]],
):
    match guardPosition:
        case (x, y, "^"):
            nextYObstacle = max([oy for ox, oy in obstacles if ox == x and oy < y])
            visited.union(map(lambda yb: (x, yb), range(y, nextYObstacle + 1)))
            guardPosition = (x, nextYObstacle + 1, ">")
            return moveGuard(guardPosition, obstacles, visited)
        case (x, y, ">"):
            nextXObstacle = min([ox for ox, oy in obstacles if oy == y and ox > x])
            visited.union(map(lambda xb: (xb, y), range(x, nextXObstacle - 1)))
            guardPosition = (nextXObstacle - 1, y, "v")
            return moveGuard(guardPosition, obstacles, visited)

        case (x, y, "v"):
            nextYObstacle = min([oy for ox, oy in obstacles if ox == x and oy > y])
            visited.union(map(lambda yb: (x, yb), range(y, nextYObstacle - 1)))
            guardPosition = (x, nextYObstacle - 1, "<")
            return moveGuard(guardPosition, obstacles, visited)
        case (x, y, "<"):
            nextXObstacle = max([ox for ox, oy in obstacles if oy == y and ox < x])
            visited.union(map(lambda xb: (xb, y), range(x, nextXObstacle + 1)))
            guardPosition = (nextXObstacle + 1, y, "^")
            return moveGuard(guardPosition, obstacles, visited)


gMap = []
startPoint = None
with open("input.txt") as file:
    for line in filter(lambda a: any(a), map(parseLine, enumerate(file.readlines()))):
        items = [(x, y, item) for x, y, item in line]
        dirPoints = list(filter(lambda xyv: xyv[2] in directionSet, items))
        if any(dirPoints):
            [startPoint] = dirPoints
        gMap.extend(items)

if startPoint is None:
    raise Exception("no start point found")
moveGuard(startPoint, gMap, set([]))
print(startPoint)
print(gMap)
