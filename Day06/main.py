from typing import Tuple

directionSet = set(["<", ">", "^", "v"])


def parse_line(linePlusIndex: Tuple[int, str]):
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


def move_guard(
    guard_position: Tuple[int, int, str],
    obstacles: list[Tuple[int, int]],
    visited: set[Tuple[int, int]],
    dimensions: Tuple[int, int],
    guard_vertices: set[Tuple[int, int, str]] = set(),
):
    # abandon the hash method as cycles could be any multiple of 4
    # instead record a list of guard positions instead and for every move check against the start of the record list and tick off each consecutive vertex
    #
    size_x, size_y = dimensions
    match guard_position:
        case (x, y, "^"):
            ys = [oy for (ox, oy) in obstacles if ox == x and oy < y]
            if len(ys) == 0:
                visited = visited.union(map(lambda vy: (x, vy), range(y, -1, -1)))
                return visited, False
            next_y_obstacle = max(ys)
            visited = visited.union(
                map(lambda yb: (x, yb), range(y, next_y_obstacle, -1))
            )
            guard_position = (x, next_y_obstacle + 1, ">")
        case (x, y, ">"):
            xs = [ox for ox, oy in obstacles if oy == y and ox > x]
            if len(xs) == 0:
                visited = visited.union(map(lambda vx: (vx, y), range(x, size_x)))
                return visited, False
            next_x_obstacle = min(xs)
            visited = visited.union(map(lambda xb: (xb, y), range(x, next_x_obstacle)))
            guard_position = (next_x_obstacle - 1, y, "v")

        case (x, y, "v"):
            ys = [oy for ox, oy in obstacles if ox == x and oy > y]
            if len(ys) == 0:
                visited = visited.union(map(lambda vy: (x, vy), range(y, size_y)))
                return visited, False
            next_y_obstacle = min(ys)
            visited = visited.union(map(lambda yb: (x, yb), range(y, next_y_obstacle)))
            guard_position = (x, next_y_obstacle - 1, "<")
        case (x, y, "<"):
            xs = [ox for ox, oy in obstacles if oy == y and ox < x]
            if len(xs) == 0:
                visited = visited.union(map(lambda vx: (vx, y), range(x, -1, -1)))
                return visited, False
            next_x_obstacle = max(xs)
            visited = visited.union(
                map(lambda xb: (xb, y), range(x, next_x_obstacle, -1))
            )
            guard_position = (next_x_obstacle + 1, y, "^")

    if guard_position in guard_vertices:
        return visited, True
    guard_vertices = guard_vertices.union([guard_position])
    return move_guard(
        guard_position,
        obstacles,
        visited,
        dimensions,
        guard_vertices=guard_vertices,
    )


def partB(visited, obstacles, guard_position, dimensions):
    loopCounter = 0
    for vx, vy in visited:
        newObstacles = []
        newObstacles.extend(obstacles)
        newObstacles.append((vx, vy))
        (_, isLoop) = move_guard(guard_position, newObstacles, set(), dimensions)
        if isLoop:
            loopCounter += 1
    return loopCounter


g_map = []
start_point = None
with open("input.txt") as file:
    lines = list(enumerate(file.readlines()))

    size_y = max([y + 1 for y, _ in lines])
    size_x = len(lines[0][1]) - 1
    for line in filter(lambda a: any(a), map(parse_line, lines)):
        items = [(x, y, item) for x, y, item in line]
        dir_points = list(filter(lambda xyv: xyv[2] in directionSet, items))
        if any(dir_points):
            [start_point] = dir_points
        g_map.extend(items)

if start_point is None:
    raise Exception("no start point found")

obstacles = [(x, y) for x, y, v in g_map if v not in directionSet]
sx, sy, _ = start_point
(results, _) = move_guard(start_point, obstacles, set([(sx, sy)]), (size_x, size_y))
print(len(results))
part_b_result = partB(results, obstacles, start_point, (size_x, size_y))
print(part_b_result)
