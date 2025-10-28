#!/usr/bin/env python3

import sys
from collections import defaultdict

counts = defaultdict(int)

for line in sys.stdin:
    code, category, count = line.strip().split("\t")
    counts[f"{code}\t{category}"] += int(count)

for key, count in counts.items():
    print(f"{key}\t{count}")
