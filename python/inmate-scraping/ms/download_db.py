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

        # will find later in parse_details_from()
        race = ''
        unit = ''

        inmates.append(Inmate(mdocid, last_name, first_name, race, location, unit))

    return inmates

def detail_url_for(mdocid):
    return DETAILS_PATH + mdocid

def enumerate_inmates(prefix):
    browser = mechanicalsoup.StatefulBrowser()

    browser.open(FORM_URL)
    browser.select_form('form')
    browser['LastName'] = prefix
    browser.submit_selected()

    page = browser.get_current_page()
    inmates = inmates_for(page)
    # return inmates
    for inmate in inmates:
        if inmate.location in ('OTHER'):
            continue
        browser.open(detail_url_for(inmate.mdocid))
        detail_page = browser.get_current_page()
        result = parse_race_and_unit_from(detail_page)
        if result:
            race, unit = result
            inmate = inmate._replace(race=race, unit=unit)
        yield inmate

    # while inmates:
        # for inmate in inmates:
            # yield inmate

def parse_race_and_unit_from(page):
    detail_table =  page.select("table")[0]
    table_rows = detail_table.find_all('tr')

    try:
        race_row = table_rows[0]
        race_cell = race_row.find_all('td')[0]
        race_cell = race_cell.get_text()
        race = race_cell.split(" ")[1]
    except:
        race = ''

    try:
        unit_row = table_rows[3]
        unit_cell = unit_row.find_all('td')[2]
        unit_cell = unit_cell.get_text()
        unit = " ".join(unit_cell.split()[1:])
    except:
        unit = ''

    return race, unit

# def race_and_unit_of(inmate):
    # response = requests.get(detail_url_for(inmate.mdocid))
    # soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)
    # detail_table =  soup.select("table")[0]
    # print(detail_table)
    # table_rows = detail_table.find_all('tr')
    # print(table_rows)

    # try:
        # race_cell = table_rows[0][0]
        # race = race_cell.split(" ")[1]
    # except:
        # race = ''

    # try:
        # unit_cell = detail_table[3][2]
        # unit = unit_cell.split(" ")
    # except:
        # unit = ''

    # return race, unit

# for prefix in ['ash']:
for prefix in string.ascii_lowercase:
    with open('data/%s.tsv' % prefix, 'w') as sink:
        sink.write('\t'.join(['mdoc_id', 'last_name', 'first_name', 'race', 'location', 'unit']))
        sink.write('\n')

        for inmate in enumerate_inmates(prefix):
            print(inmate)
            sink.write('\t'.join([inmate.mdocid, inmate.last_name, inmate.first_name, inmate.race, inmate.location, inmate.unit]))
            sink.write('\n')
            # if inmate.location in ('OTHER'):
                # continue
            # result = race_and_unit_of(inmate)
            # if result:
                # race, unit = result
                # sink.write('\t'.join([inmate.mdocid, inmate.last_name, inmate.first_name, race, inmate.location, unit]))
                # sink.write('\n')

# inmate = Inmate("38294", "", "", "" )
# print(detail_url_for(inmate.mdocid))
# print(race_and_unit_of(inmate))
