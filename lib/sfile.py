from requests import get, post
from bs4 import BeautifulSoup as bs
import json

def sfile(url):
	head = {'UserAgent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1853) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36'}
	a = bs(post(url, headers=head).text, 'html.parser')
	result = a.find('a', class_='w3-button w3-blue')
	return result