from download_inmate_details import details_for
from download_inmate_list import inmate_ids

import os
import string

DIR = 'data'

for letter in string.ascii_lowercase[15:]:
    with open(os.path.join(DIR, '%s.tsv' % letter), 'w') as tsv:
        headings = ['db_id', 'doc_id', 'sid', 'last', 'first', 'middle', 'dob', 'facility_name', 'address', 'phone']
        tsv.write('\t'.join(headings))
        tsv.write('\n')

        for db_ids in inmate_ids(letter):
            for db_id in db_ids:
                details = details_for(db_id)
                print('\t'.join(details))
                tsv.write('\t'.join(details))
                tsv.write('\n')

