#!/usr/bin/env python3

import sys

code_category = {}
with open("TNVED3.TXT", encoding="cp866") as file:
    next(file)
    for line in file:
        parts = line.strip().split("|")
        if not parts[-1]:
            code4 = parts[0] + parts[1]
            code_category[code4] = parts[2]

for line in sys.stdin:
    if line.startswith("direction"):
        continue
    code = line.strip().split("\t")[3]
    print(f"{code}\t{code_category.get(code[:4], "ПРОЧЕЕ")}\t1")
