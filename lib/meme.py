from requests import get
from bs4 import BeautifulSoup as bs

def trendcak(code):
	try:
		a = bs(get(f'https://1cak.com/{code}').text, 'html.parser')
		all = a.find('img')
		result = all['src']
		if result == 'templates/v1/img/error.png':
			return 'https://i.imgur.com/P5U7D0k.jpg'
		else:
			return result
	except Exception as e:
		return {
			'error': e
		}