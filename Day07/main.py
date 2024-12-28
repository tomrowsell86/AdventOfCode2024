from functools import partial, reduce
from typing import Tuple


def parts_acc(target: int, part_b: bool, state: Tuple[list[int], bool], part: int):
    running_totals, _ = state
    newTotals = [
        rt for rt in operation_generator(part_b, running_totals, part) if rt <= target
    ]

    return newTotals, any([a for a in newTotals if a == target])


def operation_generator(part_b, running_totals, new_value):
    for total in running_totals:
        yield total + new_value
        yield total * new_value
        if part_b:
            yield int(str(total) + str(new_value))


with open("input.txt") as file:
    part_a_total, part_b_total = 0, 0
    while line := file.readline().removesuffix("\n").replace(":", ""):
        [target, *parts] = [int(p) for p in line.split(" ")]
        (*_, part_a_matched) = list(
            reduce(partial(parts_acc, target, False), parts, ([0], False))
        )
        if part_a_matched:
            part_a_total += target

        (*_, part_b_matched) = list(
            reduce(partial(parts_acc, target, True), parts, ([0], False))
        )
        if part_b_matched:
            part_b_total += target
    print(f"Part A : {part_a_total}")
    print(f"Part B : {part_b_total}")
