import string
import mechanicalsoup
import requests
from bs4 import BeautifulSoup
import urllib
import time
from collections import namedtuple

Inmate = namedtuple('Inmate', ['dcnum', 'name', 'race', 'facility'])

FORM_URL = 'https://apps.ark.org/inmate_info/index.php'
DETAILS_PATH = 'https://apps.ark.org/inmate_info/'



def details_and_next_page_for(page):
    # Search links
    details = [a for a in page.find_all('a') if a.attrs['href'].startswith('search.php')]
    if details[0].text.startswith('Matches'):
        next_page = details[0].attrs['href']
        return details[1:], next_page
    else:
        return details, None

def detail_url_for(dcnum):
    return 'https://apps.ark.org/inmate_info/search.php?dcnum=%s' % dcnum


def enumerate_offender_dcnum():
    browser = mechanicalsoup.StatefulBrowser()

    for prefix in string.ascii_lowercase:
        browser.open(FORM_URL)
        browser.select_form('form')
        browser['lastname'] = prefix
        browser['disclaimer'] = 1
        browser['photo'] = 'nophoto'
        browser.submit_selected()

        page = browser.get_current_page()

        details, next_page = details_and_next_page_for(page)

        for detail in details:
            yield urllib.parse.parse_qs(detail.attrs['href'][11:])['dcnum'][0]

        while next_page:
            url = DETAILS_PATH + next_page
            print('<- %s' % url)
            browser.open(url)
            page = browser.get_current_page()
            details, next_page = details_and_next_page_for(page)

            for detail in details:
                yield urllib.parse.parse_qs(detail.attrs['href'][11:])['dcnum'][0]


with open('data/raw.tsv', 'w') as sink:
    sink.write('\t'.join(['adc_id', 'name', 'race', 'facility', 'address']))
    sink.write('\n')

    for dcnum in enumerate_offender_dcnum():
        time.sleep(1)

        url = detail_url_for(dcnum)

        print('<- %s' % url)

        try:
            response = requests.get(url)
        except:
            response = None

        while not response or response.status_code != 200:
            print("Server ate shit. Giving it 5 seconds.")
            time.sleep(5)
            try:
                print('<- %s' % url)
                response = requests.get(url)
            except:
                response = None

        soup = BeautifulSoup(response.text, 'html.parser')

        try:
            details = soup.select('table')[3].select('tr')
        except:
            import pdb; pdb.set_trace()
        _, _, adc_id, *_ = details[0].text.split()
        _, name = details[1].text.strip().split('\n\n')
        _, race = details[2].text.split()
        _, facility = details[10].text.strip().split('\n\n\xa0')
        _, address = details[12].text.strip().split('\n\n\xa0')

        print((adc_id, name, race, facility, address))

        sink.write('\t'.join([adc_id, name, race, facility, address]))
        sink.write('\n')

