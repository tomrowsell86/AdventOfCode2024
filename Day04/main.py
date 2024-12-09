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

            if not partB and isDirectionFromPreviousLine(pos, 0, prevLineCandidates):
                lineCandidates.append((pos, 0))

        else:
            lineCandidates.append((pos, None))

    return (False, lineCandidates)


def findWordsAcrossMultipleRows(
    cache: list[list[str]], letters: list[str], partB: bool
):
    accumulations = list(
        accumulate(zip(letters, cache), partial(lineacc, partB), initial=(True, []))
    )
    [(_, foundWordLastChars)] = accumulations[-1:]
    accumulationsReversed = list(
        accumulate(
            zip(list(reversed(letters)), cache),
            partial(lineacc, partB),
            initial=(True, []),
        )
    )
    [(_, foundWordLastCharsRev)] = accumulationsReversed[-1:]

    foundWordLastCharsRev.extend(foundWordLastChars)
    if partB:
        partBAccumulations = list(
            accumulate(
                sorted(foundWordLastCharsRev),
                partBPostSearchAccumulator,
                initial=(None, 0),
            )
        )
        [(_, count)] = partBAccumulations[-1:]
        return count
    return len(foundWordLastCharsRev)


def partBPostSearchAccumulator(
    state: Tuple[list[Tuple[int, int]] | None, int], curr: Tuple[int, int]
):
    prev, count = state
    if prev is None:
        return [curr], 0
    currPos, currDir = curr
    intersections = [
        True for p, d in prev if currPos - p == 2 and d == -1 and currDir == 1
    ]
    if any(intersections):
        count += 1
    prev.extend([curr])
    return prev, count


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
    partB = False
    searchText = "XMAS" if not partB else "MAS"
    rSearchText = "SAMX" if not partB else "SAM"
    query = list(searchText)
    buffer = []
    bufferSize = len(searchText)
    while line := file.readline().removesuffix("\n"):
        if len(buffer) < bufferSize - 1:
            buffer.append(list(line))
            if not partB:
                count += len(re.findall(searchText, line))
                count += len(re.findall(rSearchText, line))
            continue
        elif len(buffer) == bufferSize - 1:
            buffer.append(list(line))
        else:
            buffer = buffer[-(bufferSize - 1) :]
            buffer.append(list(line))

        count += findWordsAcrossMultipleRows(buffer, query, partB)
        if not partB:
            count += len(re.findall(searchText, line))
            count += len(re.findall(rSearchText, line))
