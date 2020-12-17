import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

INPUT_S = '''\
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
'''


def compute(s: str) -> int:
    count_trees = 0
    lines = s.splitlines()
    x, y = 0, 0
    step_hor = 3
    map_width = len(lines[0])
    map_height = len(lines)
    while y < map_height - 1:
        x = (x + step_hor) % map_width
        y += 1
        # breakpoint()
        if lines[y][x] == '#':
            count_trees += 1

    return count_trees


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 7),
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
