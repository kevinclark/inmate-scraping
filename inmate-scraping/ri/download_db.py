from collections import namedtuple
import os
import string

from bs4 import BeautifulSoup
import requests
import maya


import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from common.names import TWO_LETTER_PREFIXES

Inmate = namedtuple('Inmate', ['id', 'first_name', 'last_name', 'middle_name'])

DIR = 'data'
NUM_TO_GET = 20
LIST_URL =  'http://www.doc.ri.gov/family-visitors/inmate-search/search_results.php'
DETAIL_URL = 'http://www.doc.ri.gov/family-visitors/inmate-search/search_details.php?inmateid='

now = maya.now()

def cells_from_row(row):
    return row.text.strip().split('\n')

def list_inmate_and_facility(search):
    page = requests.post(LIST_URL, {'i_lname': search, 'i_nametype': 'N', 'i_agemin': 18})
    soup = BeautifulSoup(page.text, 'html.parser')
    for row in soup.find_all('tr')[1:-1]: # skip the header and footer
        cells = cells_from_row(row)
        inmate = Inmate(id=cells[1], last_name=cells[2], first_name=cells[3], middle_name=cells[4])
        yield (inmate, cells[-1])

def get_inmate_details(inmate_id):
    page = requests.get("%s%s" % (DETAIL_URL, inmate_id))
    soup = BeautifulSoup(page.text, 'html.parser')

    try:
        sentences_table = soup.find(id='sentences')
        if not sentences_table:
            return False
        sentences = sentences_table.find_all('tr')[1:]
        return any([cells_from_row(sentence)[4] in ('CONCURRENT', 'CONTROLLING SENTENCE') for sentence in sentences])
    except:
        print('\n')
        print(page.url)
        import pdb; pdb.set_trace()

facility_to_inmate = {}
seen = set()

def complete():
    return len(facility_to_inmate) >= 6 and all(len(f) >= NUM_TO_GET for f in facility_to_inmate.values())

import sys
from pprint import pprint
# Rhode Island's search is contains, not prefix
count = 0

for prefix in TWO_LETTER_PREFIXES:
    print("====== %s" % prefix)

    if complete():
        break

    for inmate, facility in list_inmate_and_facility(prefix):
        if count > 0 and count % 50 == 0:
            pprint({ f: len(i) for f, i in facility_to_inmate.items() })

        if complete():
            break

        if inmate.id in seen:
            continue

        if facility in ('SERVING OUT-OF-STATE', 'HOME CONFINEMENT'):
            continue

        if len(facility_to_inmate.get(facility, [])) <= NUM_TO_GET:
            is_incarcerated = get_inmate_details(inmate.id)
            if is_incarcerated:
                print("%s:\t%s" % (facility, inmate))
                seen.add(inmate.id)
                if facility in facility_to_inmate:
                    facility_to_inmate[facility].append(inmate)
                else:
                    facility_to_inmate[facility] = [inmate]
        count += 1

with open(os.path.join(DIR, 'inmates.tsv'), 'w') as tsv:
    headings = ['id', 'last', 'first', 'middle', 'facility_name']
    tsv.write('\t'.join(headings))
    tsv.write('\n')

    for facility, inmates in facility_to_inmate.items():
        for inmate in inmates:
            tsv.write('\t'.join([inmate.id, inmate.last_name, inmate.first_name, inmate.middle_name, facility]))
            tsv.write('\n')


