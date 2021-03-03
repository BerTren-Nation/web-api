from requests import get
from bs4 import BeautifulSoup as bs
import json

def sfile(url):
	a = bs(get(url).text, 'html.parser')
	result = a.find('a', class_='w3-button w3-blue')
	return result