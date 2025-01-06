from functools import reduce


def stone_blink_transform_gen(stones):
    for stone in stones:
        eng_text = str(stone)
        eng_length = len(list(eng_text))
        print(f"text is {eng_text} length is {eng_length}")
        if stone == 0:
            yield 1
        elif eng_length % 2 == 0:
            yield int("".join(eng_text[: int(eng_length / 2)]))
            yield int("".join(eng_text[int(eng_length / 2) :]))
        else:
            yield (stone * 2024)


def blink_reducer(stones: list[int], blink: int):
    print(f"======Blink number {blink}============")
    new_stones = [s for s in stone_blink_transform_gen(stones)]
    print(stones)
    print(f"len new stones {len(new_stones)}")
    return new_stones


with open("input.txt") as file:
    initial_stones = [
        int(s) for s in file.readline().removeprefix("\n)").split(" ") if s
    ]
    stone_count = len(reduce(blink_reducer, range(0, 25), initial_stones))
