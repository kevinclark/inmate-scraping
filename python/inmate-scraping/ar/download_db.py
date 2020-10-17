import string
import mechanicalsoup
import requests
import urllib
import time
from collections import namedtuple

Inmate = namedtuple('Inmate', ['dcnum', 'name', 'race', 'facility'])

FORM_URL = 'https://apps.ark.org/inmate_info/index.php'
LIST_URL = 'https://apps.ark.org/inmate_info/search.php'
DETAILS_PATH = 'https://apps.ark.org/inmate_info/'



def inmates_for(page):
    # Search links
    details = [a for a in page.find_all('a') if a.attrs['href'].startswith('search.php')]

    if details[0].text.startswith('Matches'):
        if details[1].text.startswith('Matches'):
            details = details[2:]
        else:
            details = details[1:]

    if len(details) == 1 and details[0].text == ',  ':
        return []

    inmates = []

    for detail in details:
        parts = detail.parent.parent.text.strip().split('\n')
        try:
            name = parts[2]
            dcnum = parts[3]
            race = parts[4]
            facility = parts[7]
        except:
            import pdb; pdb.set_trace()

        inmates.append(Inmate(dcnum, name, race, facility))

    return inmates

def detail_url_for(dcnum):
    return 'https://apps.ark.org/inmate_info/search.php?dcnum=%s' % dcnum


def enumerate_inmates(prefix):
    browser = mechanicalsoup.StatefulBrowser()

    browser.open(FORM_URL)
    browser.select_form('form')
    browser['lastname'] = prefix
    browser['disclaimer'] = 1
    browser['photo'] = 'nophoto'

    page = browser.get_current_page()
    token = page.select('input[name=token]')[0].attrs['value']

    browser.submit_selected()

    page = browser.get_current_page()

    inmates = inmates_for(browser.get_current_page())
    run = 2 # The submission gets us run 1

    while inmates:
        for inmate in inmates:
            yield inmate

        url = "%s?token=%s&lastname=%s&sex=b&photo=nophoto&disclaimer=1&RUN=%s" % (LIST_URL, token, prefix, run)
        print('<- %s' % url)
        browser.open(url)
        time.sleep(5)
        page = browser.get_current_page()
        inmates = inmates_for(page)
        if not [a for a in page.find_all('a') if a.attrs['href'].startswith('search.php') and a.text.startswith('Matches')]:
            break
        run += 1

for prefix in string.ascii_lowercase:
    with open('data/%s.tsv' % prefix, 'w') as sink:
        sink.write('\t'.join(['adc_id', 'name', 'race', 'facility']))
        sink.write('\n')

        for inmate in enumerate_inmates(prefix):
            print(inmate)

            sink.write('\t'.join([inmate.dcnum, inmate.name, inmate.race, inmate.facility]))
            sink.write('\n')

