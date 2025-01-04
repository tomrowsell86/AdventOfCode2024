from functools import reduce
from itertools import dropwhile, repeat, takewhile
from typing import NamedTuple, Tuple

Block = NamedTuple("Block", [("id", "int"), ("size", "int"), ("start_position", "int")])
Space = NamedTuple("Space", [("size", "int"), ("start_position", "int")])


def parse_and_write_out_disk_layout(input):
    id = pos = 0
    disks = []
    spaces = []
    map = []

    while True:
        disk_size = int(input.read(1))
        map.extend(repeat(id, disk_size))
        disks.append(Block(id=id, size=disk_size, start_position=pos))
        pos += disk_size
        space_size_raw = input.read(1)
        if space_size_raw and space_size_raw != "\n":
            parsed_space_size = int(space_size_raw)
            map.extend(repeat(".", parsed_space_size))
            spaces.append(Space(size=parsed_space_size, start_position=pos))
            pos += parsed_space_size
        else:
            break
        id += 1

    return (disks, spaces, map)


def checksum_reducer(state: int, item: Tuple[int, str]):
    position, id = item
    val = 0 if id == "." else int(id)
    state += position * val
    return state


with open("input.txt") as input:
    disks, spaces, map = parse_and_write_out_disk_layout(input)

    for disk in reversed(disks):
        sz = [
            (i, s)
            for i, s in dropwhile(
                lambda s: s[1].size < disk.size,
                takewhile(
                    lambda s: s[1].start_position < disk.start_position,
                    enumerate(spaces),
                ),
            )
        ]
        if len(sz):
            [(sp_index, s), *_] = sz

            for i, c in enumerate(repeat(disk.id, disk.size)):
                map[s.start_position + i] = c

            for i, c in enumerate(repeat(".", disk.size)):
                map[disk.start_position + i] = c
                spaces[sp_index] = Space(
                    size=(s.size - disk.size),
                    start_position=s.start_position + disk.size,
                )
    result = reduce(checksum_reducer, enumerate(map), 0)
    print(result)
