import argparse
import csv
import os.path
import re
from typing import Dict

import pytest

from support import timing

'''
You can continue to ignore the cid field, but each other field has strict
rules about what values are valid for automatic validation:

    byr (Birth Year) - four digits; at least 1920 and at most 2002.
    iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    hgt (Height) - a number followed by either cm or in:
        If cm, the number must be at least 150 and at most 193.
        If in, the number must be at least 59 and at most 76.
    hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    pid (Passport ID) - a nine-digit number, including leading zeroes.
    cid (Country ID) - ignored, missing or not.

Your job is to count the passports where all required fields are both present
and valid according to the above rules. Here are some example values:

byr valid:   2002
byr invalid: 2003

hgt valid:   60in
hgt valid:   190cm
hgt invalid: 190in
hgt invalid: 190

hcl valid:   #123abc
hcl invalid: #123abz
hcl invalid: 123abc

ecl valid:   brn
ecl invalid: wat

pid valid:   000000001
pid invalid: 0123456789
'''

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

REQUIRED_FIELDS = frozenset(('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'))


def compute(s: str) -> int:
    count_valid = 0
    fieldnames = sorted(REQUIRED_FIELDS)
    fieldnames.append('cid')
    with open('valid_passports.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        breakpoint()
        writer.writeheader()
        for passport in s.split('\n\n'):
            fields_list = [s.strip().split(':') for s in passport.split()]
            fields = {k: v for k, v in fields_list}
            if passport_is_valid(fields):
                count_valid += 1
                writer.writerow(fields)
    return count_valid


def passport_is_valid(fields: Dict[str, str]) -> bool:
    # breakpoint()
    if not set(fields.keys()).issuperset(REQUIRED_FIELDS):
        return False
    datecondition = (2020 <= int(fields['eyr']) <= 2030 and
                     1920 <= int(fields['byr']) <= 2002 and
                     2010 <= int(fields['iyr']) <= 2020)
    if not datecondition:
        return False
    if not re.match(r'^\d{9}$', fields['pid']):
        return False
    if not (
        (height_match := re.match(r'(\d+)(in|cm)$', fields['hgt'])) and
        (
            (height_match[2] == 'cm' and 150 <= int(height_match[1]) <= 193) or
            (height_match[2] == 'in' and 59 <= int(height_match[1]) <= 76)
        )
    ):
        return False

    if not re.match('#[0-9a-f]{6}', fields['hcl']):
        return False
    if not fields['ecl'] in set('amb blu brn gry grn hzl oth'.split()):
        return False
    return True
#


INPUT_S_INVALID = '''\
        eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007

'''
INPUT_S_VALID = '''\
pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719


'''

INPUT_S = INPUT_S_VALID + INPUT_S_INVALID

# Preparation for testing passport_is_valid
VALID_PASSPORTS = INPUT_S_VALID.split('\n\n')
INVALID_PASSPORTS = INPUT_S_INVALID.split('\n\n')


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        # put given test cases here
        (INPUT_S, 4),
    )
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


@pytest.mark.parametrize(
    ('passport', 'expected'),
    (
        (VALID_PASSPORTS[0], True),
        (VALID_PASSPORTS[1], True),
        (VALID_PASSPORTS[2], True),
        (VALID_PASSPORTS[3], True),

        (INVALID_PASSPORTS[0], False),
        (INVALID_PASSPORTS[1], False),
        (INVALID_PASSPORTS[2], False),
        (INVALID_PASSPORTS[3], False),
    )
)
def test_passport_is_valid(passport: str, expected: bool) -> None:
    fields_list = [s.strip().split(':') for s in passport.split()]
    fields = {k: v for k, v in fields_list}
    assert passport_is_valid(fields) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
