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


with open("input.txt", "r") as file:
    updateFollow = {}
    while line := file.readline().removesuffix("\n"):
        [v, k] = line.split("|")
        if k not in updateFollow:
            updateFollow[k] = []
        updateFollow[k].append(v)

    partA = 0
    while line := file.readline().removesuffix("\n"):
        updates = list(map(int, line.split(",")))
        head = updates[0]
        tail = updates[1:]
        isCorrect = scanUpdates(head, tail, updateFollow)
        if isCorrect:
            partA += updates[floor(len(updates) / 2)]
    print(partA)
