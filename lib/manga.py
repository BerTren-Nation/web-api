from requests import get
from bs4 import BeautifulSoup as bs

def scrap_komiku(url):
    try:
        ko = bs(get(f'https://data1.komiku.id{url}').content, 'html.parser')
        thumb = ko.find('div', class_='ims').img['src']
        info_ = ko.find('table', class_='inftable').findAll('td')
        info = ''
        for i in range(len(info_)):
            if i == 0: info += f'{info_[i].text} : {info_[i+1].text}\n'
            elif i % 2 == 0 and info_[i].text not in info: info += f'{info_[i].text} : '
            elif i % 2 != 0 and info_[i].text not in info: info += f'{info_[i].text}\n'
        return {
						'thumb': thumb,
        				'info': info
        			}
    except Exception as e:
        return {
            'error': e,
            'msg': 'Failed get metadata'
        }

def search_komiku(query):
    try:
        url = bs(get('https://data1.komiku.id/cari/?post_type=manga&s=%s' % query).text, 'html.parser').find('div', class_='bge').a['href']
        return url
    except Exception as e:
        return ('Manga %s Tidak di temukan!' % e)
