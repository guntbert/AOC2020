import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    count_correct_passwords = 0
    for line in s.splitlines():
        rule, char, pw = line.split()
        rule_start_s, rule_end_s = rule.split('-')
        min_count, max_count = int(rule_start_s), int(rule_end_s)
        char = char[0]

        char_count = 0
        for c in pw:
            if c == char:
                char_count += 1
        if min_count <= char_count <= max_count:
            count_correct_passwords += 1
    return count_correct_passwords


INPUT_S = '''\
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 2),
    ),
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
