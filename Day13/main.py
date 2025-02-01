from typing import NamedTuple

Point = NamedTuple("Point", [("x", int), ("y", int)])
ClawMachine = NamedTuple(
    "ClawMachine",
    [
        ("button_a", Point),
        ("button_b", Point),
        ("prize_location", Point),
    ],
)


def parse_coordinates(line: str):
    x = line.replace(",", "").split(" ")[2].split("+")[1]
    y = line.split(" ")[3].split("+")[1]
    return Point(int(x), int(y))


def extract_claw_params(block: list[str], part_b=False):
    a, b, prize, *_ = block
    [px, py] = [
        (10000000000000 if part_b else 0) + int(p.replace(",", "").split("=")[1])
        for p in prize.split(" ")[1:]
    ]
    return ClawMachine(parse_coordinates(a), parse_coordinates(b), Point(px, py))


def calculate_fewest_tokens_for_prize(cm: ClawMachine):
    yb = cm.button_a.x * cm.button_b.y
    ya = cm.button_b.x * cm.button_a.y
    b_target = cm.button_a.y * cm.prize_location.x
    a_target = cm.button_a.x * cm.prize_location.y
    b_presses_q, b_presses_remainder = divmod(abs(a_target - b_target), abs(yb - ya))

    if b_presses_remainder == 0:
        a_presses_q, a_presses_remainder = divmod(
            (cm.prize_location.x - b_presses_q * cm.button_b.x), (cm.button_a.x)
        )

        return b_presses_q + a_presses_q * 3 if a_presses_remainder == 0 else 0
    return 0


with open("input.txt") as file:
    claw_machines_a = [
        extract_claw_params(b.split("\n"), part_b=False)
        for b in (file.read().split("\n\n"))
    ]

    file.seek(0)

    claw_machines_b = [
        extract_claw_params(b.split("\n"), part_b=True)
        for b in (file.read().split("\n\n"))
    ]
    token_total_a, token_total_b = (0, 0)
    for cm in claw_machines_a:
        token_total_a += calculate_fewest_tokens_for_prize(cm)
    for cm in claw_machines_b:
        token_total_b += calculate_fewest_tokens_for_prize(cm)
    print(f"part a result : {token_total_a}")
    print(f"part b result: {token_total_b}")
