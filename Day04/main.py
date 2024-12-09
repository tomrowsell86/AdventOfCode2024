from itertools import accumulate
from functools import partial
from typing import Tuple
import re


def lineacc(
    partB: bool,
    state: Tuple[bool, list[Tuple[int, int | None]]],
    current: Tuple[str, list[str]],
):
    ch, line = current
    init, prevLineCandidates = state
    if not any(prevLineCandidates) and not init:
        return state
    lineCandidates = []
    for pos in [i for c, i in zip(line, range(0, len(line))) if c == ch]:
        if any(prevLineCandidates):
            if isDirectionFromPreviousLine(pos, -1, prevLineCandidates):
                lineCandidates.append((pos, -1))

            if isDirectionFromPreviousLine(pos, 1, prevLineCandidates):
                lineCandidates.append((pos, 1))

            if isDirectionFromPreviousLine(pos, 0, prevLineCandidates):
                lineCandidates.append((pos, 0))
        else:
            lineCandidates.append((pos, None))
    return (False, lineCandidates)


def findWordsAcrossMultipleRows(cache: list[list[str]], letters: list[str]):
    accumulations = list(
        accumulate(zip(letters, cache), partial(lineacc, False), initial=(True, []))
    )
    [(_, foundWordLastChars)] = accumulations[-1:]
    return len(foundWordLastChars)


def isDirectionFromPreviousLine(
    currentPosition: int, direction: int, candidates: list[Tuple[int, int | None]]
):
    return any(
        [
            True
            for a, d in candidates
            if currentPosition - (direction) == a and (d is None or d == direction)
        ]
    )


with open("input.txt", "r") as file:
    count = 0
    query, rquery = (list("XMAS"), list("SAMX"))
    #   for line in map(lambda _: file.readline().removesuffix("\n"), range(0, 4)):
    #       cache.append(list(line))
    #       count += len(re.findall("(XMAS)", line))
    #       count += len(re.findall("(SAMX)", line))
    #
    #   count += findWordsAcrossMultipleRows(cache, query)
    #   count += findWordsAcrossMultipleRows(cache, rquery)
    buffer = []
    while line := file.readline().removesuffix("\n"):
        if len(buffer) < 3:
            buffer.append(list(line))
            count += len(re.findall("(XMAS)", line))
            count += len(re.findall("(SAMX)", line))
            continue
        elif len(buffer) == 3:
            buffer.append(list(line))
        else:
            buffer = buffer[-3:]
            buffer.append(list(line))

        count += findWordsAcrossMultipleRows(buffer, query)
        count += findWordsAcrossMultipleRows(buffer, rquery)
        count += len(re.findall("(XMAS)", line))
        count += len(re.findall("(SAMX)", line))

print(count)
