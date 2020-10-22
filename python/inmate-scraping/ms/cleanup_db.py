import string

with open('data/all_cleaned.tsv', 'w') as sink:
    headers_added = False
    for prefix in string.ascii_lowercase:
        print('data/%s.tsv' % prefix)
        with open('data/%s.tsv' % prefix) as source:
            for line_no, line in enumerate(source):
                if line_no == 0:
                    # Deal with headers from other files
                    if not headers_added:
                        headers = line.split('\t')
                        sink.write('\t'.join(headers))
                        sink.write('\n')
                        headers_added = True
                    continue

                mdoc_id, last_name, first_name, location = line.strip().split('\t')

                if 'OTHER' in location:
                    continue

                sink.write('\t'.join([mdoc_id, last_name, first_name, location]))
                sink.write('\n')
