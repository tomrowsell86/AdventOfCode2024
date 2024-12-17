from typing import Tuple

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
    print(guardPosition)
    match guardPosition:
        case (x, y, "^"):
            ys = [oy for (ox, oy) in obstacles if ox == x and oy < y]
            if not len(ys):
                return visited
            nextYObstacle = max(ys)
            visited = visited.union(
                map(lambda yb: (x, yb), range(y, nextYObstacle, -1))
            )
            guardPosition = (x, nextYObstacle + 1, ">")
            return moveGuard(guardPosition, obstacles, visited)
        case (x, y, ">"):
            ys = [ox for ox, oy in obstacles if oy == y and ox > x]
            if not any(ys):
                return visited
            nextXObstacle = min(ys)
            visited = visited.union(map(lambda xb: (xb, y), range(x, nextXObstacle)))
            guardPosition = (nextXObstacle - 1, y, "v")
            return moveGuard(guardPosition, obstacles, visited)

        case (x, y, "v"):
            ys = [oy for ox, oy in obstacles if ox == x and oy > y]
            if not any(ys):
                return visited
            nextYObstacle = min(ys)
            visited = visited.union(map(lambda yb: (x, yb), range(y, nextYObstacle)))
            guardPosition = (x, nextYObstacle - 1, "<")
            return moveGuard(guardPosition, obstacles, visited)
        case (x, y, "<"):
            ys = [ox for ox, oy in obstacles if oy == y and ox < x]
            if not any(ys):
                return visited
            nextXObstacle = max(ys)
            visited = visited.union(
                map(lambda xb: (xb, y), range(x, nextXObstacle, -1))
            )
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

sx, sy, _ = startPoint
results = moveGuard(
    startPoint, [(x, y) for x, y, v in gMap if v not in directionSet], set([(sx, sy)])
)
