import requests
from bs4 import BeautifulSoup
import time

def address_for(adc_id):
    print('<- Facility for %s' % adc_id)
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

# TODO
# Write location/address matching function

with open('data/cleaned.tsv', 'w') as sink:
    headers_added = False
    for prefix in string.ascii_lowercase:
        with open('data/$s.tsv' % prefix) as source:
            for line_no, line in enumerate(source):
                if line_no == 0:
                    # Deal with headers from other files
                    if not headers_added:
                        headers = line.split('\t')
                        headers.append('race')
                        headers.append('address')
                        sink.write('\t'.join(headers))
                        sink.write('\n')
                        headers_added = True
                    continue

                mdoc_id, last_name, first_name, race, location, unit = line.strip().split('\t')

                if 'OTHER' in location:
                    continue

                address = address_for(location)
                if not address:
                    continue

                sink.write('\t'.join([mdoc_id, last_name, first_name, location, race, address]))
                sink.write('\n')
