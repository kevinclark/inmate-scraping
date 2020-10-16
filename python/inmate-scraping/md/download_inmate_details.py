import requests
import string
import re
import time
import os
from bs4 import BeautifulSoup
from urllib.parse import parse_qs, urlparse

DETAIL_URL = "http://www.dpscs.state.md.us/inmate/search.do?searchType=detail&id="

CLICK_TEXT = r"Please click on the facility name to see its details. Eastern Correctional Institution/Annex"

def detail_url(db_id):
    return "%s%s" % (DETAIL_URL, db_id)

def details_for(db_id):
    url = detail_url(db_id)
    print("->: %s" % url)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    rows = soup.find_all('tr')

    try:
        sid, last, first, middle, dob = [cell.text.strip() for cell in rows[9].find_all('td')]
    except:
        import pdb; pdb.set_trace()

    doc_id, facility_block = [r.text.strip() for r in rows[11].find_all('td')]

    try:
        _, facility_name, address_and_phone = facility_block.split('\n\n')
    except:
        facility_name = ''
        address_and_phone = ''

    try:
        cleaned = re.sub(r' *Address:\xa0\xa0', '\t', address_and_phone)
        cleaned = re.sub(r' *Phone:\xa0\xa0', '\t', cleaned)

        address, phone = [t.strip() for t in cleaned.strip().split('\t')]
    except:
        address = ''
        phone = ''


    return [db_id, doc_id, sid, last, first, middle, dob, facility_name, address, phone]
