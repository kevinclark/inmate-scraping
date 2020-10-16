"""
Pull 150 inmates total from institutions outside of baltimore
"""

import os
import random

candidates = []

with open(os.path.join('data', 'cleaned.tsv')) as source:
    with open(os.path.join('data', 'sampled.tsv'), 'w') as sink:
        # Skip anyone who doesn't have a doc_id
        for line_no, line in enumerate(source):
            if line_no == 0:
                sink.write(line)
                continue

            _, doc_id, _, _, _, _, _, _, address, _ = line.split('\t')

            if doc_id and 'Baltimore' not in address:
                candidates.append(line)

        # Now sample 150
        for line in random.choices(candidates, k=150):
            sink.write(line)

