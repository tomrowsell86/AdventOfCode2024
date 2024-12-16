from math import floor


def scanUpdates(hd, tl, orderDict):
    if not any(tl):
        return True
    else:
        if str(hd) in orderDict and any(
            [t for t in tl if any([d for d in orderDict[str(hd)] if d == str(t)])]
        ):
            return False
        else:
            return scanUpdates(tl[0], tl[1:], orderDict)


def sortedUpdates(updates: list[int], orderLookup: dict[str, set[str]]):
    if len(updates) == 1:
        return updates
    hd = updates[0]
    newUpdates = sortedUpdates(updates[1:], orderLookup)
    hdPos = 0
    for i, u in enumerate(newUpdates):
        if hd not in orderLookup or u in orderLookup[str(hd)]:
            newUpdates[i] = hd
            newUpdates[hdPos] = u
            hdPos = i

    return newUpdates


with open("input.txt", "r") as file:
    updateFollow: dict[str, set[str]] = {}
    while line := file.readline().removesuffix("\n"):
        [v, k] = line.split("|")
        if k not in updateFollow:
            updateFollow[k] = set([])
        updateFollow[k].add(v)

    partB = 0
    partA = 0
    while line := file.readline().removesuffix("\n"):
        updates: list[int] = list(map(int, line.split(",")))
        head = updates[0]
        tail = updates[1:]
        isCorrect = scanUpdates(head, tail, updateFollow)
        if isCorrect:
            partA += updates[floor(len(updates) / 2)]
        else:
            sUpdates = sortedUpdates(updates, updateFollow)
            print(sUpdates)
            partB += sUpdates[floor(len(sUpdates) / 2)]

    print(partA)
    print(partB)
