#!/usr/bin/env python3

import sys

total = 0
prev_code = None
prev_category = None


def print_result():
    print(f"{prev_code}\t{total}\t{prev_category}")


for line in sys.stdin:
    code, category, count = line.strip().split("\t")
    if code != prev_code and prev_code is not None:
        print_result()
        total = 0
    total += int(count)
    prev_code = code
    prev_category = category

if prev_code:
    print_result()
