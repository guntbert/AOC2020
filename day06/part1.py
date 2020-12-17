import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    sum_yes_per_grup = 0
    for group in s.split('\n\n'):
        yes_answers = set(''.join(group).replace('\n', ''))
        sum_yes_per_grup += len(yes_answers)
    # TODO: implement solution here!
    return sum_yes_per_grup


INPUT_S = '''\
abc

a
b
c

ab
ac

a
a
a
a

b
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        # put given test cases here
        (INPUT_S, 11),
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
