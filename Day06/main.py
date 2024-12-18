from typing import Tuple
from collections import deque

directionSet = set(["<", ">", "^", "v"])


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
    dimensions: Tuple[int, int],
    lastEightVertices: deque[Tuple[int, int]] = deque(maxlen=8),
):
    # abandon the hash method as cycles could be any multiple of 4
    # instead record a list of guard positions instead and for every move check against the start of the record list and tick off each consecutive vertex
    #
    print(lastEightVertices)
    primeFactors = [13, 5, 7, 11]
    if len(lastEightVertices) == 8:
        hashValFirstFour = sum(
            [p * x * y for p, (x, y) in zip(primeFactors, lastEightVertices)]
        )
        hashValLastFour = sum(
            [p * x * y for p, (x, y) in zip(primeFactors, list(lastEightVertices)[-4:])]
        )
        print("hash of first four: %s %s" % (hashValFirstFour, hashValLastFour))
        if hashValFirstFour == hashValLastFour:
            print("matched!!!!!!!!!!!!!!")
            return visited, True

    sizeX, sizeY = dimensions
    match guardPosition:
        case (x, y, "^"):
            ys = [oy for (ox, oy) in obstacles if ox == x and oy < y]
            if len(ys) == 0:
                visited = visited.union(map(lambda vy: (x, vy), range(y, -1, -1)))
                return visited, False
            nextYObstacle = max(ys)
            visited = visited.union(
                map(lambda yb: (x, yb), range(y, nextYObstacle, -1))
            )
            guardPosition = (x, nextYObstacle + 1, ">")
        case (x, y, ">"):
            xs = [ox for ox, oy in obstacles if oy == y and ox > x]
            if len(xs) == 0:
                visited = visited.union(map(lambda vx: (vx, y), range(x, sizeX)))
                return visited, False
            nextXObstacle = min(xs)
            visited = visited.union(map(lambda xb: (xb, y), range(x, nextXObstacle)))
            guardPosition = (nextXObstacle - 1, y, "v")

        case (x, y, "v"):
            ys = [oy for ox, oy in obstacles if ox == x and oy > y]
            if len(ys) == 0:
                visited = visited.union(map(lambda vy: (x, vy), range(y, sizeY)))
                return visited, False
            nextYObstacle = min(ys)
            visited = visited.union(map(lambda yb: (x, yb), range(y, nextYObstacle)))
            guardPosition = (x, nextYObstacle - 1, "<")
        case (x, y, "<"):
            xs = [ox for ox, oy in obstacles if oy == y and ox < x]
            if len(xs) == 0:
                visited = visited.union(map(lambda vx: (vx, y), range(x, -1, -1)))
                return visited, False
            nextXObstacle = max(xs)
            visited = visited.union(
                map(lambda xb: (xb, y), range(x, nextXObstacle, -1))
            )
            guardPosition = (nextXObstacle + 1, y, "^")
    lastEightVertices.append((guardPosition[0], guardPosition[1]))
    return moveGuard(
        guardPosition,
        obstacles,
        visited,
        dimensions,
        lastEightVertices=lastEightVertices,
    )


def partB(visited, obstacles, guardPosition, dimensions):
    loopCounter = 0
    dq = deque(maxlen=8)
    for vx, vy in visited:
        print("%s %s" % (vx, vy))
        newObstacles = []
        newObstacles.extend(obstacles)
        newObstacles.append((vx, vy))
        (_, isLoop) = moveGuard(
            guardPosition, newObstacles, set(), dimensions, lastEightVertices=dq
        )
        if isLoop:
            loopCounter = loopCounter + 1
        dq.clear()
    return loopCounter


gMap = []
startPoint = None
with open("input.txt") as file:
    lines = list(enumerate(file.readlines()))

    sizeY = max([y + 1 for y, _ in lines])
    sizeX = len(lines[0][1]) - 1
    for line in filter(lambda a: any(a), map(parseLine, lines)):
        items = [(x, y, item) for x, y, item in line]
        dirPoints = list(filter(lambda xyv: xyv[2] in directionSet, items))
        if any(dirPoints):
            [startPoint] = dirPoints
        gMap.extend(items)

if startPoint is None:
    raise Exception("no start point found")

obstacles = [(x, y) for x, y, v in gMap if v not in directionSet]
sx, sy, _ = startPoint
(results, _) = moveGuard(startPoint, obstacles, set([(sx, sy)]), (sizeX, sizeY))
print("partB starting ==============")
partBResult = partB(results, obstacles, startPoint, (sizeX, sizeY))
print(partBResult)
print(len(results))
