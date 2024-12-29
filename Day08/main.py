from functools import reduce, partial


def antenna_reducer(part_b, bounds, state, item):
    map, seen = state
    kx, ky, v, _ = item
    co_frequency_antennas = [
        (x, y) for x, y, c, _ in map if c == v and (x, y) != (kx, ky)
    ]

    def within_bounds(x, y):
        return x >= 0 and x < bounds and y >= 0 and y < bounds

    for cx, cy in co_frequency_antennas:
        dx, dy = (cx - kx, cy - ky)
        an_x = kx - dx
        an_y = ky - dy
        if part_b:
            seen.add((cx, cy))

        if within_bounds(an_x, an_y):
            seen.add((an_x, an_y))

        if part_b:
            an_x -= dx
            an_y -= dy

            while within_bounds(an_x, an_y):
                seen.add((an_x, an_y))
                an_x -= dx
                an_y -= dy

    return (map, seen)


with open("input.txt", "r") as file:
    antenna_map = [
        (x, y, c, len(line))
        for y, line in enumerate((ln.removesuffix("\n") for ln in file.readlines()))
        for x, c in enumerate(list(line))
        if c != "."
    ]
    [(*_, bounds), *_] = antenna_map
    _, anti_nodes_a = reduce(
        partial(antenna_reducer, False, bounds), antenna_map, (antenna_map, set())
    )

    _, anti_nodes_b = reduce(
        partial(antenna_reducer, True, bounds), antenna_map, (antenna_map, set())
    )
    print(f"Part A: {len(anti_nodes_a)}")
    print(f"Part B: {len(anti_nodes_b)}")
