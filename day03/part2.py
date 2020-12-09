import argparse
import os.path

from typing import List

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

def _compute(lines: List[str], x_step: int, y_step: int) -> int:
    count_trees = 0
    x, y = 0, 0
    map_width = len(lines[0])
    map_height = len(lines)
    while y < map_height - 1:
        x = (x + x_step) % map_width
        y += y_step
        #breakpoint()
        if lines[y][x] == '#':
            count_trees += 1

    return count_trees


def compute(s: str) -> int:
    lines =  s.splitlines()

    return (
            _compute( lines, 1, 1) *
            _compute( lines, 3, 1) *
            _compute( lines, 5, 1) *
            _compute( lines, 7, 1) *
            _compute( lines, 1, 2) 
            )


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
      (INPUT_S, 336),
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
