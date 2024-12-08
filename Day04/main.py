from itertools import accumulate
from typing import Tuple
import re


def lineacc(
    state: Tuple[bool, list[Tuple[int, int | None]]], current: Tuple[str, list[str]]
):
    ch, line = current
    init, prevLineCandidates = state
    if not any(prevLineCandidates) and not init:
        return state
    lineCandidates = []
    for pos in [i for c, i in zip(line, range(0, len(line))) if c == ch]:
        if any(prevLineCandidates):
            forward = any(
                [
                    "a"
                    for a, d in prevLineCandidates
                    if pos - 1 == a and (d is None or d == 1)
                ]
            )
            backward = any(
                [
                    "a"
                    for a, d in prevLineCandidates
                    if a == pos + 1 and (d == -1 or d is None)
                ]
            )
            down = any(
                [
                    "a"
                    for a, d in prevLineCandidates
                    if a == pos and (d == 0 or d is None)
                ]
            )
            #            if pos == 1:
            #                print(prevLineCandidates)
            #                print(forward)
            #                print(backward)
            if backward:
                lineCandidates.append((pos, -1))

            if forward:
                lineCandidates.append((pos, 1))

            if down:
                lineCandidates.append((pos, 0))
        else:
            lineCandidates.append((pos, None))
    return (False, lineCandidates)


def findWords(cache: list[list[str]], letters: list[str]):
    accResult = list(accumulate(zip(letters, cache), lineacc, initial=(True, [])))
    [last] = accResult[-1:]
    _, tmp = last
    return len(tmp)


with open("input.txt", "r") as file:
    cache = []
    count = 0
    query, rquery = (list("XMAS"), list("SAMX"))
    for line in map(lambda _: file.readline().removesuffix("\n"), range(0, 4)):
        cache.append(list(line))
        count += len(re.findall("(XMAS)", line))
        count += len(re.findall("(SAMX)", line))

    count += findWords(cache, query)

    count += findWords(cache, rquery)

    while line := file.readline().removesuffix("\n"):
        print("==================================")
        cache = cache[-3:]
        cache.append(list(line))
        count += findWords(cache, query)
        count += findWords(cache, rquery)
        count += len(re.findall("(XMAS)", line))
        count += len(re.findall("(SAMX)", line))


print(count)
