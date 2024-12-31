from io import TextIOWrapper
from itertools import groupby, repeat
from functools import reduce, partial
from typing import Tuple


class Block:
    size: int
    type: str

    def __init__(self, size, type):
        self.size = size
        self.type = type


def disk_map_gen(handle: TextIOWrapper):
    while (disk := handle.read(1)) and disk != "\n":
        yield Block(int(disk), "d")
        if (space := handle.read(1)) and space != "\n":
            yield Block(int(space), "s")


def compact_disks_reducer(
    spaces_count: int,
    state: Tuple[list[str], list[Tuple[int, Block]]],
    block: Tuple[int, Block],
):
    compacted_disks, spaces = state
    (id, bl) = block
    exhausted_spaces = []
    for sid, sp in spaces:
        while sp.size > 0 and bl.size > 0 and len(compacted_disks) < (spaces_count - 1):
            compacted_disks.append(str(id))
            sp.size -= 1
            bl.size -= 1
        if sp.size == 0:
            exhausted_spaces.append(sid)

    return (
        compacted_disks,
        [(id, s) for id, s in spaces if id not in exhausted_spaces],
    )


def checksum_reducer(state: int, item: Tuple[int, str]):
    position, id = item
    state += position * int(id)
    return state


with open("input.txt") as file:
    [disk_map, space_map] = [
        list(enumerate(g))
        for _, g in groupby(
            sorted(disk_map_gen(file), key=lambda b: b.type), lambda b: b.type
        )
    ]

    space_count = sum([s.size for _, s in space_map])
    disk_count = sum([s.size for _, s in disk_map])
    fills, sp = reduce(
        partial(compact_disks_reducer, space_count),
        sorted(disk_map, reverse=True),
        ([], space_map),
    )
    file.seek(0)
    fills.reverse()

    rendered_layout = [
        fills.pop() if b == "." and len(fills) > 0 else b
        for a in (
            list(repeat("." if b.type == "s" else str(int(id / 2)), b.size))
            for id, b in enumerate(disk_map_gen(file))
        )
        for b in a
        if len(fills) > 0
    ][:disk_count]

    checksum = reduce(checksum_reducer, enumerate(rendered_layout), 0)
    print(checksum)
