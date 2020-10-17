import requests
from bs4 import BeautifulSoup
import time

def details_for(adc_id):
    return 'https://apps.ark.org/inmate_info/search.php?dcnum=%s' % adc_id

def address_for(adc_id):
    time.sleep(3)

    print('<- Facility for %s' % adc_id)
    response = requests.get(details_for(adc_id))
    soup = BeautifulSoup(response.text, 'html.parser')
    row = [tr for tr in soup.select('tr') if tr.text.strip().startswith('Facility')][0]
    _, address_part = row.text.strip().split('\n\n\xa0')
    if 'N/A' == address_part:
        return None

    try:
        address, _ = address_part.split('\xa0')
    except:
        import pdb; pdb.set_trace()

    return address.strip()

addresses = {}

with open('data/cleaned.tsv', 'w') as sink:
    with open('data/raw.tsv') as source:
        for line_no, line in enumerate(source):
            if line_no == 0:
                headers = line.split('\t')
                headers.append('address')
                sink.write('\t'.join(headers))
                sink.write('\n')
                continue

            adc_id, name, race, facility = line.strip().split('\t')

            if 'Waiting List' in facility:
                continue

            if facility not in addresses:
                addresses[facility] = address_for(adc_id)

            address = addresses[facility]

            if not address:
                continue

            sink.write('\t'.join([adc_id, name, race, facility, address]))
            sink.write('\n')
