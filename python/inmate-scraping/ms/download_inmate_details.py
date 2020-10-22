import string
import mechanicalsoup
from bs4 import BeautifulSoup
import requests
import urllib
import time
from collections import namedtuple

InmateDetail = namedtuple('InmateDetail', ['mdoc_id', 'last_name', 'first_name', 'race', 'location', 'unit'])

FORM_URL = 'https://www.ms.gov/mdoc/inmate/Search/Index'
LIST_URL = 'https://www.ms.gov/mdoc/inmate/Search/GetSearchResults'
DETAILS_PATH = 'https://www.ms.gov/mdoc/inmate/Search/GetDetails/'

def detail_url_for(mdocid):
    return DETAILS_PATH + mdocid

def open_db_search():
    browser = mechanicalsoup.StatefulBrowser()

    browser.open(FORM_URL)
    browser.select_form('form')
    browser['LastName'] = "a"
    browser.submit_selected()
    return browser

def parse_race_and_unit_from(page):
    try:
        detail_table =  page.select("table")[0]
        table_rows = detail_table.find_all('tr')

        race_row = table_rows[0]
        race_cell = race_row.find_all('td')[0]
        race_cell = race_cell.get_text()
        race = race_cell.split(" ")[1]

        unit_row = table_rows[3]
        unit_cell = unit_row.find_all('td')[2]
        unit_cell = unit_cell.get_text()
        unit = " ".join(unit_cell.split()[1:])
    except:
        print("No details table found. Details page returned:")
        print(page)
        race = ''
        unit = ''

    return race, unit

def find_details_for(inmate, browser):
    browser.open(detail_url_for(inmate.mdoc_id))
    detail_page = browser.get_current_page()
    result = parse_race_and_unit_from(detail_page)
    if result:
        race, unit = result
        inmate = inmate._replace(race=race, unit=unit)
    return inmate


with open('data/inmate_details.tsv', 'w') as sink:
    with open('data/sampled_facilities.tsv') as source:
        browser = open_db_search()
        for line_no, line in enumerate(source):
            if line_no == 0:
                # Deal with headers
                sink.write('\t'.join(['mdoc_id', 'last_name', 'first_name', 'race', 'location', 'unit']))
                sink.write('\n')
                continue

            mdoc_id, last_name, first_name, location = line.strip().split('\t')
            race = ''
            unit = ''
            inmate = InmateDetail(mdoc_id, last_name, first_name, race, location, unit)
            inmate = find_details_for(inmate, browser)
            print(inmate)
            sink.write('\t'.join([inmate.mdoc_id, inmate.last_name, inmate.first_name, inmate.race, inmate.location, inmate.unit]))
            sink.write('\n')

# inmate = Inmate("38294", "", "", "" )
# print(detail_url_for(inmate.mdocid))
# print(race_and_unit_of(inmate))
