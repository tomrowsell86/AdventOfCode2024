from math import floor


def scanUpdates(hd, tl, orderDict):
    if not any(tl):
        return True
    else:
        if hd in orderDict and any(
            [t for t in tl if any([d for d in orderDict[hd] if d == t])]
        ):
            return False
        else:
            return scanUpdates(tl[0], tl[1:], orderDict)


def sortedUpdates(updates: list[int], orderLookup: dict[int, set[int]]):
    if len(updates) == 1:
        return updates
    hd = updates[0]
    newUpdates = sortedUpdates(updates[1:], orderLookup)
    hdPos = -1
    fstItem = hd
    for i, update in enumerate(newUpdates):
        if hd in orderLookup and update in orderLookup[hd]:
            if hdPos == -1:
                fstItem = update
            else:
                newUpdates[hdPos] = update
            newUpdates[i] = hd
            hdPos = i
    newUpdates.insert(0, fstItem)
    return newUpdates


with open("input.txt", "r") as file:
    updatePrecededByLookup: dict[int, set[int]] = {}
    while line := file.readline().removesuffix("\n"):
        precededBy, update = map(int, line.split("|"))
        if update not in updatePrecededByLookup:
            updatePrecededByLookup[update] = set([])
        updatePrecededByLookup[update].add(precededBy)

    partB, partA = (0, 0)
    while line := file.readline().removesuffix("\n"):
        updates: list[int] = list(map(int, line.split(",")))
        head = updates[0]
        tail = updates[1:]
        isCorrect = scanUpdates(head, tail, updatePrecededByLookup)
        if isCorrect:
            partA += updates[floor(len(updates) / 2)]
        else:
            sUpdates = sortedUpdates(updates, updatePrecededByLookup)
            partB += sUpdates[floor(len(sUpdates) / 2)]

    print(partA)
    print(partB)
