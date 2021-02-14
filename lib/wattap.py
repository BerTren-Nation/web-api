from requests import get
from bs4 import BeautifulSoup as bs

def wattap_i(query):
    url = bs(get(query).text, 'html.parser').findAll('p')
    return url