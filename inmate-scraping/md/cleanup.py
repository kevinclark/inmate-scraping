import os

with open(os.path.join('data', 'cleaned.tsv'), 'w') as sink:
    headings = ['db_id', 'doc_id', 'sid', 'last', 'first', 'middle', 'dob', 'facility_name', 'address', 'phone']
    sink.write('\t'.join(headings))
    sink.write('\n')

    with open(os.path.join('data', 'deduped.tsv')) as source:
        for line_no, line in enumerate(source):
            if line_no == 0:
                continue

            parts = line.split('\t')

            facility_name = parts[7]

            if not facility_name or facility_name in ('Youth Detention Center', 'Central Home Detention Unit'):
                continue

            sink.write(line)


