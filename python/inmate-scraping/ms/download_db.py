import string
import mechanicalsoup
from bs4 import BeautifulSoup
import requests
import urllib
import time
from collections import namedtuple

Inmate = namedtuple('Inmate', ['mdocid', 'last_name', 'first_name', 'race', 'location', 'unit'])

FORM_URL = 'https://www.ms.gov/mdoc/inmate/Search/Index'
LIST_URL = 'https://www.ms.gov/mdoc/inmate/Search/GetSearchResults'
DETAILS_PATH = 'https://www.ms.gov/mdoc/inmate/Search/GetDetails/'



def inmates_for(page):
    inmates = []
    
    # Parse table
    table = page.table
    table_rows = table.find_all('tr')
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        # Skip if empty row for headers etc.
        if len(row) == 0: 
            continue
        if "No inmates found matching your criteria" in row:
            return []

        try:
            mdocid = row[0]
            last_name = row[1]
            first_name = row[2]
            location = row[3]
        except:
            import pdb; pdb.set_trace()

        inmates.append(Inmate(mdocid, last_name, first_name, location))

    return inmates

def enumerate_inmates(prefix):
    browser = mechanicalsoup.StatefulBrowser()

    browser.open(FORM_URL)
    browser.select_form('form')
    browser['LastName'] = prefix
    browser.submit_selected()

    page = browser.get_current_page()
    inmates = inmates_for(page)
    return inmates

# for prefix in ['ash']:
for prefix in string.ascii_lowercase:
    with open('data/%s.tsv' % prefix, 'w') as sink:
        sink.write('\t'.join(['mdoc_id', 'last_name', 'first_name', 'location']))
        sink.write('\n')

        for inmate in enumerate_inmates(prefix):
            print(inmate)
            sink.write('\t'.join([inmate.mdocid, inmate.last_name, inmate.first_name, inmate.location]))
            sink.write('\n')

# inmate = Inmate("38294", "", "", "" )
# print(detail_url_for(inmate.mdocid))
# print(race_and_unit_of(inmate))
