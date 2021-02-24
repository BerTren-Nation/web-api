from requests import get
from bs4 import BeautifulSoup as bs

def pencarian_countdown(search):
	try:
		awal=bs(get(f'https://yourcountdown.to/everything?search={search}&approved=1&tags=&tag_match_type=any&confirmed_status=any&order=most_popular').content, 'html.parser')
		result = awal.find('div', class_='countdown list')
		info = awal.find('div', class_='content')
		return {
						'time': result['data-date'],
						'title': info.find('h4', class_="title").text
					}
	except Exception as e:
		return {
						'status': False,
						'error': e
					}