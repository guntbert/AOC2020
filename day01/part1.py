import argparse

import pytest

from support import timing


def compute(s: str) -> int:
    numbers = [int(n_s) for n_s in s.split()]
    length = len(numbers)
    #breakpoint()
    for pos_n1, n1  in enumerate(numbers):
      pos_n2 = pos_n1 + 1
      while pos_n2 < length:
        n2 = numbers[pos_n2]
        if n1 + n2 == 2020:
          return n1* n2
        pos_n2 += 1
         


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('1721 979 366 299 675 1456', 514579),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file')
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
