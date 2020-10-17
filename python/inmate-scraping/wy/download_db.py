import sys
import os
import json
from collections import namedtuple

from bs4 import BeautifulSoup
import mechanicalsoup
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from common.names import TWO_LETTER_PREFIXES

FORM_URL = 'http://wdoc-loc.wyo.gov/'
DATA_URL = 'http://wdoc-loc.wyo.gov/Home/getInmateList'
DETAIL_URL = 'http://wdoc-loc.wyo.gov/Home/Detail/?id=32547&dbType=WCIS'

Offender = namedtuple('Offender', ['id', 'docId', 'first', 'last',
                                   'age', 'gender', 'groupKind', 'fromDB'])


def detail_url(offender_id, db):
    return 'http://wdoc-loc.wyo.gov/Home/Detail/?id=%s&dbType=%s' % (offender_id, db)

def enumerate_offenders():
    browser = mechanicalsoup.StatefulBrowser()

    for prefix in TWO_LETTER_PREFIXES:
        browser.open(FORM_URL)
        browser.select_form('form')
        browser['lastName'] = prefix

        browser.submit_selected()

        browser.open(DATA_URL)

        docIdsSeen = set()

        offenders = json.loads(browser.get_current_page().find('p').text)['data']

        for o in offenders:
            if o['docID'] not in docIdsSeen and o['fromDB'] not in ('MONITOR'):
                offender = Offender(o['offenderID'], o['docID'], o['firstName'].strip(), o['lastName'].strip(),
                               o['age'], o['gender'], o['groupKind'], o['fromDB'])

                docIdsSeen.add(offender.id)
                yield offender


def race_facility_and_race_of(offender):
    response = requests.get(detail_url(offender.id, offender.fromDB))
    soup = BeautifulSoup(response.text, 'html.parser')
    left_detail =  soup.select(".detailLeftBaseContainer tr:nth-of-type(6) td:nth-of-type(2)")[0]
    facility_name = left_detail.contents[0]

    if facility_name in ('In Custody'):
        return None

    try:
        addr = left_detail.contents[2]
        city, _, zip_ = left_detail.contents[4].split()
    except:
        addr = ''
        city = ''
        zip_ = ''

    race = soup.select('.detailRightBaseContainer tr:nth-of-type(2) td:nth-of-type(2)')[0].text

    return race, facility_name, addr, city, zip_



with open(os.path.join('data', 'raw.tsv'), 'w') as sink:
    sink.write('\t'.join(['docId', 'first', 'last', 'race', 'facility', 'address', 'city', 'zip']))
    sink.write('\n')

    for o in enumerate_offenders():
        print(o)
        result = race_facility_and_race_of(o)
        if result:
            race, facility, address, city, zip_  = result
            sink.write('\t'.join([str(o.docId), o.first, o.last, race, facility, address, city, zip_]))
            sink.write('\n')


