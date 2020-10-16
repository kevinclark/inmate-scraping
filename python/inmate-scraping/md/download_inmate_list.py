import requests
import string
import time
import os
from bs4 import BeautifulSoup
from urllib.parse import parse_qs, urlparse

LIST_URL = "http://www.dpscs.state.md.us/inmate/search.do?searchType=name&firstnm=&lastnm="

def list_url(letter, start=1):
    return "%s%s&start=%s" % (LIST_URL, letter, start)


def ids_for(letter, row_id):
    url = list_url(letter, row_id)
    print("->: %s" % url)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    ids = []
    for link in soup.find_all('a'):
        url = urlparse(link['href'])
        if url.path == 'search.do':
            # This is a detail
            parsed = parse_qs(url.query)
            ids.append(parsed['id'][0])

    return ids


def inmate_ids(letter):
    row_id = 1

    ids = ids_for(letter, row_id)

    while ids:

        yield ids

        row_id += len(ids)
        ids = ids_for(letter, row_id)
