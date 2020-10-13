import string
import os
import sys

inmates = {}

for letter in string.ascii_lowercase:
    with open(os.path.join('data', '%s.tsv' % letter)) as letter_tsv:
        for line_no, line in enumerate(letter_tsv):
            sys.stdout.write('.')
            if line_no == 0:
                continue

            parts = line.split('\t')
            key = (parts[3], parts[4], parts[5], parts[6]) # name and dob
            if not key:
                import pdb; pdb.set_trace()

            if key in inmates:
                merged = inmates[key]
                for i, part in enumerate(parts):
                    if not merged[i]:
                        merged[i] = part
                inmates[key] = merged
            else:
                inmates[key] = parts
    sys.stdout.flush()

rows = sorted(inmates.values(), key=lambda x: (x[3], x[4]))

with open(os.path.join('data', 'deduped.tsv'), 'w') as tsv:
    headings = ['db_id', 'doc_id', 'sid', 'last', 'first', 'middle', 'dob', 'facility_name', 'address', 'phone']
    tsv.write('\t'.join(headings))
    tsv.write('\n')

    for row in rows:
        tsv.write('\t'.join(row))

