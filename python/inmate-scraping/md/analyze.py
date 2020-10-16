import os
counter = {}

with open(os.path.join('data', 'cleaned.tsv')) as tsv:
    for line_no, line in enumerate(tsv):
        if line_no == 0:
            continue

        parts = line.split('\t')

        if not parts[1]:
            counter[parts[7]] = counter.get(parts[7], 0) + 1

import pprint;
pprint.pprint(counter)

