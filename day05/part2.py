import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    empty_seat_ids = [i for i in range(2**10)]
    for line in s.splitlines():
        seat_id = int(line.translate(str.maketrans('BFRL', '1010', '')), 2)
        empty_seat_ids.remove(seat_id)
    for id in empty_seat_ids:
        if id - 1 in empty_seat_ids or id + 1 in empty_seat_ids:
            continue
        return id
    raise AssertionError('should not be reached')


INPUT_S = '''\
BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        # put given test cases here
        (INPUT_S, 820),
    )
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
