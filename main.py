#from lib.pytube import YouTube
from lib.dewa import cari
from lib.anime import *
from lib.brainly import *
from lib.manga import *
from lib.resize import *
from lib.search import *
from lib.nulis import *
from lib.meme import *
from urllib.parse import *
from flask import *
#from werkzeug.utils import *
from functools import wraps
from googletrans import Translator
from bs4 import BeautifulSoup as bs
from requests import get, post, Session
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
import os, math, json, random, re, html_text, pytesseract, base64, time, smtplib, string

ua_ig = 'Mozilla/5.0 (Linux; Android 9; SM-A102U Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 Instagram 155.0.0.37.107 Android (28/9; 320dpi; 720x1468; samsung; SM-A102U; a10e; exynos7885; en_US; 239490550)'

app = Flask(__name__)
client = FaunaClient(secret="fnAECDM_y6ACB0IddJ-dSMwtXAEuZP7AaaQrs8nz")
translator = Translator()
apiKey = 'O8mUD3YrHIy9KM1fMRjamw8eg'
apiKey_ocr = '09731daace88957'
app.config['MEDIA'] = 'tts'
app.secret_key = b'BB,^z\x90\x88?\xcf\xbb'
#ALLOWED_EXTENSION = set(['png', 'jpeg', 'jpg'])
#app.config['Layer_Folder'] = 'layer'

def generate_identifier(n=6):
    identifier = ""
    for i in range(n):
        identifier += random.choice(string.ascii_letters)
    return identifier

HTTP_STATUS_CODES = {
    100: "Continue",
    101: "Switching Protocols",
    102: "Processing",
    103: "Early Hints",  # see RFC 8297
    200: "OK",
    201: "Created",
    202: "Accepted",
    203: "Non Authoritative Information",
    204: "No Content",
    205: "Reset Content",
    206: "Partial Content",
    207: "Multi Status",
    208: "Already Reported",  # see RFC 5842
    226: "IM Used",  # see RFC 3229
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Found",
    303: "See Other",
    304: "Not Modified",
    305: "Use Proxy",
    306: "Switch Proxy",  # unused
    307: "Temporary Redirect",
    308: "Permanent Redirect",
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",  # unused
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Timeout",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    412: "Precondition Failed",
    413: "Request Entity Too Large",
    414: "Request URI Too Long",
    415: "Unsupported Media Type",
    416: "Requested Range Not Satisfiable",
    417: "Expectation Failed",
    418: "I'm a teapot",  # see RFC 2324
    421: "Misdirected Request",  # see RFC 7540
    422: "Unprocessable Entity",
    423: "Locked",
    424: "Failed Dependency",
    425: "Too Early",  # see RFC 8470
    426: "Upgrade Required",
    428: "Precondition Required",  # see RFC 6585
    429: "Too Many Requests",
    431: "Request Header Fields Too Large",
    449: "Retry With",  # proprietary MS extension
    451: "Unavailable For Legal Reasons",
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
    505: "HTTP Version Not Supported",
    506: "Variant Also Negotiates",  # see RFC 2295
    507: "Insufficient Storage",
    508: "Loop Detected",  # see RFC 5842
    510: "Not Extended",
    511: "Network Authentication Failed",  # see RFC 6585
}

def short_url(address):
    identifier = generate_identifier()
    client.query(q.create(q.collection("urls"), {
        "data": {
            "identifier": identifier,
            "url": address
        }
    }))
    shortened_url = request.host_url + identifier
    return shortened_url

def convert_size(size_bytes):
	if size_bytes == 0:
		return '0B'
	size_name = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
	i = int(math.floor(math.log(size_bytes, 1024)))
	p = math.pow(1024, i)
	s = round(size_bytes / p, 2)
	return '%s %s' % (s, size_name[i])

def apikey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
    	try:
    		if request.args.get('apikey'):
    			keyy = client.query(q.get(q.match(q.index("Neko"), request.args.get('apikey'))))
    			return view_function(*args, **kwargs)
    		else:
    			return 'Masukan Apikey'
    	except Exception as e:
    		print(e)
    		return { 'status': False, 'pesan': 'Apikey Invalid'}
    return decorated_function

#def allowed_file(filename):
#    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION
@app.route("/api/translate", methods=['GET','POST'])
def translate():
	text = request.args.get('text')
	language = request.args.get('language')
	result = translator.translate(f'{text}', dest=language)
	print(result)
	return result

@app.route("/api/npm", methods=['GET','POST'])
@apikey
def npm():
	if request.args.get("apikey"):
		try:
			url = f'https://api.npms.io/v2/search?q={request.args.get("q")}'
			result = get(url).json()
			return {'status': 200, 'total': result["total"], 'result': result['result'] }
		except Exception as e:
			print(e)
			return {'error': 'Emror'}
	else:
		return { 'status': False, 'pesan': 'Masukkan parameter q'}

@app.route("/api/shortlink", methods=['GET','POST'])
def generate():
	if request.args.get('link'):
    	identifier = os.urandom(20).hex()
    	client.query(q.create(q.collection("urls"), {
        	"data": {
        		"identifier": identifier,
            	"url": request.args.get('link')
        	}
    	}))

    	shortened_url = f'{request.host_url}g/{identifier}'
    	return jsonify({"status": 200, "url": shortened_url})
    else:
    	return { 'status': False, 'pesan': 'Masukkan parameter link'}

@app.route("/g/<string:identifier>/", methods=['GET','POST'])
def fetch_original(identifier):
    try:
        url = client.query(q.get(q.match(q.index("Neko"), identifier)))
    except:
        return { 'status': False, 'pesan': 'Tidak Di Temukan Code'}

    return redirect(url["data"]["url"])

@app.route('/api/statuscode', methods=['GET','POST'])
@apikey
def statuscode():
	if request.args.get('code'):
		try:
			code = int(request.args.get('code'))
			return { 'status': 200, 'result': HTTP_STATUS_CODES[code] }
		except Exception as e:
			return { 'status': 200, 'result': 'Tidak Ada Code Respon'}
	else:
		return { 'status': False, 'pesan': 'Masukkan parameter code'}

@app.route('/api/simi', methods=['GET','POST'])
@apikey
def simi():
	if request.args.get('text'):
		if request.args.get('language'):
			simi_txt = request.args.get('text')
			simi_language = request.args.get('language')
			simi_url = f'http://api.simsimi.com/request.p?key=ae752867-ab2f-4827-ab64-88aebed49a1c&lc={simi_language}&text={simi_txt}'
			result = get(simi_url).json()
			return { 'status': 200, 'result': result['response'] }
		else:
			return { 'status': False, 'pesan': 'Masukkan parameter language'}
	else:
		return { 'status': False, 'pesan': 'Masukkan parameter text'}

@app.route('/api/husbu', methods=['GET','POST'])
@apikey
def husbu():
	husbu_file = json.loads(open('husbu.json').read())
	result = random.choice(husbu_file)
	return { 'status': 200, 'result': result }

@app.route('/api/1cak', methods=['GET','POST'])
@apikey
def onecak():
	if request.args.get('code'):
		try:
			code = int(request.args.get('code'))
			result = trendcak(code)
			return { 'status': 200, 'result': result }
		except Exception as e:
			return { 'status': False, 'pesan': 'Error{e}'}
	else:
		return {
			'status': False,
			'pesan': '[!] Masukkan parameter code'
		}

@app.route('/api/r1cak', methods=['GET','POST'])
def trenonecak():
	result = trendcak(random.randint(1111110,9987199))
	return { 'status': 200, 'result': result }

@app.route('/admin/file/cyser/<path:filename>', methods=['GET','POST'])
def sendFille(filename):
	try:
		return send_from_directory(app.config['MEDIA'], filename, as_attachment=True)
	except Exception as e:
		return render_template('404.html'), 404

@app.route('/api/layer', methods=['GET','POST'])
def layer():
	if request.args.get('base64image'):
		try:
			open('piw.jpg','w').write(request.args.get('base64image'))
			os.system('base64 -i -d piw.jpg > paw.jpg')
			hehe = resizeTo('paw.jpg')
			huhu = layer(hehe, 'black')
			os.system('base64 result.jpg > pow.jpg')
			return {
				'status': 200,
				'result': '`data:image/jpg;base64,%s`' % open('pow.jpg').read()
			}
		except Exception as e:
			print(e)
			#os.remove('piw.jpg')
			return {
				'status': False,
				'error': '[!] Invalid base64 image!'
			}
	else:
		return {
			'status': False,
			'pesan': '[!] Masukkan parameter base64image'
		}

@app.route('/api/spamgmail', methods=['GET','POST'])
@apikey
def spamgimel():
    if request.args.get('target'):
        if request.args.get('jum'):
            abece = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
            target_imel = request.args.get('target')
            jumlah = int(request.args.get('jum'))
            if jumlah > 10:
                return {
                    'status': False,
                    'pesan': '[!] Max 10 tod!'
                }
            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.ehlo()
                server.starttls()
                server.login('spamz.cyser@gmail.com', 'spamz cyser 888')
                hasil = ''
                for i in range(jumlah):
                    mess = ''.join(random.choice(abece) for _ in range(4))
                    msg = f'From: {random.randint(1, 100)}<Hacker>\nSubject: Anonymous ~ Hacker\n{mess}'
                    server.sendmail('spamz.cyser@gmail.com', target_imel, msg)
                    hasil += '[!] Sukses\n'
                server.quit()
                return {
                    'status': 200,
                    'logs': hasil
                }
            except Exception as e:
                print(e)
                hasil = '[!] Gagal'
                return {
                    'status': False,
                    'logs': hasil
                }
        else:
            return {
                'status': False,
                'pesan': 'Masukkan parameter jum'
            }
    else:
        return {
            'status': False,
            'pesan': 'Masukkan parameter target'
        }

@app.route('/api/spamcall', methods=['GET','POST'])
@apikey
def spamcall():
    if request.args.get('no'):
        no = request.args.get('no')
        if str(no).startswith('8'):
            hasil = ''
            kyaa = post('https://id.jagreward.com/member/verify-mobile/%s' % no).json()
            print(kyaa['message'])
            if 'Anda akan menerima' in kyaa['message']:
                hasil += '[!] Berhasil mengirim spam call ke nomor : 62%s' % no
            else:
                hasil += '[!] Gagal mengirim spam call ke nomor : 62%s' % no
            return {
                'status': 200,
                'logs': hasil
            }
        else:
            return {
                'status': False,
                'pesan': '[!] Tolong masukkan nomor dengan awalan 8'
            }
    else:
        return {
            'status': False,
            'pesan': '[!] Masukkan parameter no' 
        }
@app.route('/api/spamsms', methods=['GET','POST'])
@apikey
def spamming():
    if request.args.get('no'):
        if request.args.get('jum'):
            no = request.args.get('no')
            jum = int(request.args.get('jum'))
            if jum > 20: return {
                'status': 200,
                'pesan': '[!] Max 20 ganteng'
            }
            url = 'https://www.lpoint.co.id/app/member/ESYMBRJOTPSEND.do'
            head = {'UserAgent': 'Mozilla/5.0 (Linux; Android 8.1.0; CPH1853) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36'}
            data = {'pn': '',
                'bird': '',
                'webMbrId': '',
                'webPwd': '',
                'maFemDvC': '',
                'cellNo': no,
                'otpNo': '',
                'seq': '',
                'otpChk': 'N',
                'count': ''
            }
            hasil = ''
            for i in range(jum):
                kyaa = post(url, headers=head, data=data).text
                if 'error' in kyaa:
                    hasil += '[!] Gagal\n'
                else:
                    hasil += '[!] Sukses\n'
            return {
                'status': 200,
                'logs': hasil
            }
        else:
            return {
                'status': False,
                'pesan': '[!] Masukkin parameter jum juga ganteng'
            }
    else:
        return {
            'status': False,
            'pesan': '[!] Masukkan parameter no'
        }

@app.route('/nulis', methods=['GET','POST'])
@apikey
def noolees():
    if request.args.get('text'):
        try:
            nulis = tulis(unquote(request.args.get('text')))
            for i in nulis:
                i.save('resolt.jpg')
            return {
                'status': 200,
                'result': imageToBase64('resolt.jpg')
            }
        except:
            return {
                'status': False,
                'error': 'Failed writing dude:('
            }
    else:
        return {
            'status': False,
            'pesan': '[!] Masukkan parameter text'
        }
@app.route('/api/wiki', methods=['GET','POST'])
@apikey
def wikipedia():
	if request.args.get('q'):
		try:
			kya = request.args.get('q')
			cih = f'https://id.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles={kya}'
			heuh = get(cih).json()
			heuh_ = heuh['query']['pages']
			hueh = re.findall(r'(\d+)', str(heuh_))
			result = heuh_[hueh[0]]['extract']
			return {
				'status': 200,
				'result': result
			}
		except Exception as e:
			print(e)
			return {
				'status': False,
				'error': '[❗] Yang anda cari tidak bisa saya temukan di wikipedia!'
			}
	else:
		return {
			'status': False,
			'pesan': '[!] Masukkan param q'
		}

@app.route('/api/tts', methods=['GET','POST'])
@apikey
def tts():
	if request.args.get('text'):
		try:
			teks = request.args.get('text')
			print(teks)
			if int(len(teks)) - int(len(teks.split(' '))) == 250:
				return {
					'status': 200,
					'pesan': '[❗] Maaf teks terlalu panjang!!',
				}
			else:
				url = f'https://rest.farzain.com/api/tts.php?id={teks}&apikey='
				if os.path.isfile('./tts/tts.mp3') == True:
					os.remove('./tts/tts.mp3')
					Tts = get(f'{url}{apiKey}').content
					open('tts/tts.mp3','wb').write(Tts)
					return {
						'status': 200,
						'pesan': 'Success convert text to speech!',
						'file': 'https://mhankbarbar/tts/tts.mp3'
					}
				else:
					Tts = get(f'{url}{apiKey}').content
					open('tts/tts.mp3','wb').write(Tts)
					return {
						'status': 200,
						'pesan': 'Success convert text to speech!',
						'file': 'https://mhankbarbar.herokuapp.com/tts/tts.mp3'
					}
		except Exception as e:
			print(e)
			return {
				'status': False,
				'pesan': '[!] Upss, terjadi kesalahan'
			}
	else:
		return {
			'status': 200,
			'pesan': '[!] Masukkan parameter text'
		}

@app.route('/api/ytv', methods=['GET','POST'])
@apikey
def ytv():
	if request.args.get('url'):
		try:
			url = request.args.get('url').replace('[','').replace(']','')
			ytv = post('https://www.y2mate.com/mates/en60/analyze/ajax',data={'url':url,'q_auto':'0','ajax':'1'}).json()
			yaha = bs(ytv['result'], 'html.parser').findAll('td')
			filesize = yaha[len(yaha)-23].text
			id = re.findall('var k__id = "(.*?)"', ytv['result'])
			thumb = bs(ytv['result'], 'html.parser').find('img')['src']
			title = bs(ytv['result'], 'html.parser').find('b').text
			dl_link = bs(post('https://www.y2mate.com/mates/en60/convert',data={'type':url.split('/')[2],'_id':id[0],'v_id':url.split('/')[3],'ajax':'1','token':'','ftype':'mp4','fquality':'360p'}).json()['result'],'html.parser').find('a')['href']
			return {
				'status': 200,
				'title': title,
				'thumb': thumb,
				'result': dl_link,
				'resolution': '360p',
				'filesize': filesize,
				'ext': 'mp4'
			}
		except Exception as e:
			print('Error : %s ' % e)
			return {
				'status': False,
				'error': '[❗] Terjadi kesalahan, mungkin link yang anda kirim tidak valid!'
			}
	else:
		return {
			'status': False,
			'pesan': 'Masukkan parameter url'
		}

@app.route('/api/yta', methods=['GET','POST'])
@apikey
def yta():
	if request.args.get('url'):
		try:
			url = request.args.get('url').replace('[','').replace(']','')
			yta = post('https://www.y2mate.com/mates/en60/analyze/ajax',data={'url':url,'q_auto':'0','ajax':'1'}).json()
			yaha = bs(yta['result'], 'html.parser').findAll('td')
			filesize = yaha[len(yaha)-10].text
			id = re.findall('var k__id = "(.*?)"', yta['result'])
			thumb = bs(yta['result'], 'html.parser').find('img')['src']
			title = bs(yta['result'], 'html.parser').find('b').text
			dl_link = bs(post('https://www.y2mate.com/mates/en60/convert',data={'type':url.split('/')[2],'_id':id[0],'v_id':url.split('/')[3],'ajax':'1','token':'','ftype':'mp3','fquality':'128'}).json()['result'],'html.parser').find('a')['href']
			return {
				'status': 200,
				'title': title,
				'thumb': thumb,
				'filesize': filesize,
				'result': dl_link,
				'ext': 'mp3'
			}
		except Exception as e:
			print('Error : %s' % e)
			return {
				'status': False,
				'error': '[❗] Terjadi kesalahan mungkin link yang anda kirim tidak valid!'
			}
	else:
		return {
			'status': False,
			'pesan': '[!] Masukkan parameter url'
		}

@app.route('/api/chord', methods=['GET','POST'])
@apikey
def chord():
	if request.args.get('q'):
		try:
			q = request.args.get('q').replace(' ','+')
			id = get('http://app.chordindonesia.com/?json=get_search_results&exclude=date,modified,attachments,comment_count,comment_status,thumbnail,thumbnail_images,author,excerpt,content,categories,tags,comments,custom_fields&search=%s' % q).json()['posts'][0]['id']
			chord = get('http://app.chordindonesia.com/?json=get_post&id=%s' % id).json()
			result = html_text.parse_html(chord['post']['content']).text_content()
			return {
				'status': 200,
				'result': result
			}
		except Exception as e:
			print(e)
			return {
				'status': False,
				'error': '[❗] Maaf chord yang anda cari tidak dapat saya temukan!'
			}
	else:
		return {
			'status': False,
			'pesan': '[!] Masukkan parameter q'
		}

@app.route('/api/dewabatch', methods=['GET','POST'])
@apikey
def dewabatch():
	if request.args.get('q'):
		try:
			q = request.args.get('q')
			he=search_dewabatch(quote(q))
			dewabatch=cari(he)
			if he != '':
				return {
					'status': 200,
					'sinopsis': dewabatch['result'],
					'thumb': dewabatch['cover'],
					'result': dewabatch['info']
				}
		except Exception as e:
			print(e)
			return {
				'status': False,
				'error': 'Anime %s Tidak di temukan!' % unquote(q)
			}
	else:
		return {
			'status': False,
			'pesan': '[!] Masukkan parameter q'
		}

@app.route('/api/komiku', methods=['GET','POST'])
@apikey
def komiku():
    if request.args.get('q'):
        try:
            q = request.args.get('q')
            komi = search_komiku(q)
            print(komi)
            if 'Tidak di temukan' not in komi:
                manga = scrap_komiku(komi)
                print(manga)
                return {
                    'status': 200,
                    'thumb': manga['thumb'],
                    'info': manga['info']
                }
        except Exception as e:
            print(e)
            return {
                'status': False,
                'error': 'Manga %s Tidak di temukan' % unquote(q)
            }
    else:
        return {
            'status': False,
            'pesan': '[!] Masukkan parameter q'
        }

@app.route('/api/kuso', methods=['GET','POST'])
@apikey
def kusonime():
	if request.args.get('q'):
		try:
			q = request.args.get('q')
			he=search_kusonime(quote(q))
			kuso=scrap_kusonime(he)
			if he != '':
				return {
					'status': 200,
					'sinopsis': kuso['sinopsis'],
					'thumb': kuso['thumb'],
					'info': kuso['info'],
					'title': kuso['title'],
					'link_dl': kuso['link_dl']
				}
		except Exception as e:
			print(e)
			return {
				'status': False,
				'error': 'Anime %s Tidak di temukan' % unquote(q)
			}
	else:
		return {
			'status': False,
			'pesan': '[!] Masukkan parameter q'
		}

@app.route('/api/otakudesu')
@apikey
def otakudesuu():
    if request.args.get('q'):
        try:
            q = request.args.get('q')
            he=search_otakudesu(quote(q))
            if he != '':
                otaku=scrap_otakudesu(he)
                return {
                    'status': 200,
                    'sinopsis': otaku['sinopsis'],
                    'thumb': otaku['thumb'],
                    'info': otaku['info'],
                    'title': otaku['title']
                }
        except Exception as e:
            print(e)
            return {
                'status': False,
                'error': 'Anime %s Tidak di temukan' % unquote(q)
            }
    else:
        return {
            'status': False,
            'pesan': '[!] Masukkan parameter q'
        }
            
@app.route('/api/brainly', methods=['GET','POST'])
@apikey
def brainly_scraper():
	if request.args.get('q'):
		try:
			query = request.args.get('q')
			br=brainly(gsearch('"%s" site:brainly.co.id' % quote(query), lang='id')[0])
			return {
				'status': 200,
				'result': br
			}
		except Exception as e:
			print(e)
			return {
				'status': False,
				'error': '[❗] Pertanyaan %s tidak dapat saya temukan di brainly' % unquote(query)
			}
	else:
		return {
			'status': False,
			'pesan': '[!] Masukkan parameter q'
		}

@app.route('/api/nekonime', methods=['GET','POST'])
@apikey
def nekonimek():
	try:
		neko = get('https://waifu.pics/api/sfw/neko').json()
		nimek = neko['url']
		result = short_url(nimek)
		return {
			'status': 200,
			'result': result
		}
	except:
		neko = get('https://waifu.pics/api/sfw/neko').json()
		nimek = neko['url']
		result = short_url(nimek)
		return {
			'status': 200,
			'result': result
		}

@app.route('/api/randomloli', methods=['GET','POST'])
@apikey
def randomloli():
	try:
		hehe = ['kawaii','neko']
		loli = get('https://api.lolis.life/%s' % random.choice(hehe)).json()['url']
		return {
			'status': 200,
			'result': loli
		}
	except:
		return {
			'status': 200,
			'result': loli
		}
@app.route('/api/ig', methods=['GET','POST'])
@apikey
def igeh():
	if request.args.get('url'):
		try:
			url = request.args.get('url')
			data = {'id': url}
			result = get('https://www.villahollanda.com/api.php?url=' + url).json()
			if result['descriptionc'] == None:
				return {
					'status': False,
					'result': 'https://c4.wallpaperflare.com/wallpaper/976/117/318/anime-girls-404-not-found-glowing-eyes-girls-frontline-wallpaper-preview.jpg',
				}
			else:
				return {
					'status': 200,
					'result': result['descriptionc'],
				}
		except Exception as e:
			print(e)
			return {
				'status': False,
				'result': 'https://c4.wallpaperflare.com/wallpaper/976/117/318/anime-girls-404-not-found-glowing-eyes-girls-frontline-wallpaper-preview.jpg',
				'error': True
			}
	else:
		return {
			'status': False,
			'pesan': '[!] Masukkan parameter url'
		}

@app.route('/api/cuaca', methods=['GET','POST'])
@apikey
def cuaca():
	if request.args.get('q'):
		try:
			q = request.args.get('q')
			print(q)
			url = f'https://rest.farzain.com/api/cuaca.php?id={q}&apikey='
			weather = get(f'{url}{apiKey}').json()
			print(weather)
			if weather['respon']['deskripsi'] == 'null' or weather['respon']['deskripsi'] == None:
				return {
					'status': 404,
					'error': '[❗] Gagal mengambil informasi cuaca, mungkin tempat tidak terdaftar/salah!'
				}
			else:
				return {
					'status': 200,
					'result': {
						'tempat': weather['respon']['tempat'],
						'cuaca': weather['respon']['cuaca'],
						'desk': weather['respon']['deskripsi'],
						'suhu': weather['respon']['suhu'],
						'kelembapan': weather['respon']['kelembapan'],
						'udara': weather['respon']['udara'],
						'angin': weather['respon']['angin']
					}
				}
		except Exception as e:
			print('Error : %s' % e)
			return {
				'status': False,
				'pesan': '[❗] Gagal mengambil informasi cuaca, mungkin tempat tidak terdaftar/salah!'
			}
	else:
		return {
			'status': False,
			'pesan': '[!] Masukkan parameter q'
		}

@app.route('/api/stalk', methods=['GET','POST'])
def stalk():
	if request.args.get('username'):
		try:
			username = request.args.get('username').replace('@','')
			igestalk = bs(get('https://www.mystalk.net/profile/%s' % username, headers={'User-Agent':'Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36'}).text, 'html.parser').find('div', class_='user-profile-area')
			igestalk_ = igestalk.findAll('span')
			thumb = igestalk.find('img')['src']
			return {
				'status': 200,
				'Name': igestalk_[0].text.strip(),
				'Username': igestalk_[1].text.strip(),
				'Jumlah_Post': igestalk_[2].text.replace('\n',' ').strip(),
				'Jumlah_Followers': igestalk_[3].text.replace('\n',' ').strip(),
				'Jumlah_Following': igestalk_[4].text.replace('\n',' ').strip(),
				'Biodata': igestalk.find('p').text.strip(),
				'Profile_pic': thumb
			}
		except Exception as e:
			print(e)
			return {
				'status': False,
				'error': '[❗] Username salah!!'
			}
	else:
		return {
			'status': False,
			'pesan': '[!] Masukkan parameter username'
		}

@app.route('/daerah', methods=['GET','POST'])
def daerah():
	daerah = 'Andreas, Ambon, Amlapura, Alford, Argamakmur, Atambua, Babo, Bagan Siapiapi, Central Kalimantan, Birmingham, Samosir, Balikpapan, Banda Aceh, Bandar Lampung, Bandung, Bangkalan, Cianjur, Bangko, Bangli, Banjar, Banjar Baru, Banjarmasin, Corn, BANTAENG , Banten, Bantul, Banyuwangi, Barabai, Barito, Barru, Batam, Batang, Batu, Baturaja, Batusangkar, Baubau, Bekasi, Bengkalis, Bengkulu, Benteng, Biak, Bima, Binjai, Bireuen, Bitung, Blitar, Blora, Bogor, Bojonegoro , Bondowoso, Bontang, Boyolali, Brebes, Bukit Tinggi, Maluku, Bulukumba, Buntok, Cepu, Ciamis, Cianjur, Cibinong, Cilacap, Cilegon, Cimahi, Cirebon, Curup, Demak, Denpasar, Depok, Dili, Dompu, Donggala, Dumai, Ende, Enggano, Enrekang, Fakfak, Garut, Gianyar, Gombong, Gorontalo, Gresik, Gunung Sitoli, Indramayu, Jakarta Barat, Jakarta Pusat, Jakarta Selatan, Jakarta Timur, Jakarta Utara, Jambi,Jayapura, Jember, Jeneponto, Jepara, Jombang, Kabanjahe, Kalabahi, Kalianda, Kandangan, Karanganyar, Karawang, Kasungan, Kayuagung, Kebumen, Kediri, Kefamenanu, Kendal, Kendari, Kertosono, Ketapang, Kisaran, Klaten, Kolaka, Kota Baru Pulau Laut , Bumi Bumi, Kota Jantho, Kotamobagu, Kuala Kapuas, Kuala Kurun, Kuala Pembuang, Kuala Tungkal, Kudus, Kuningan, Kupang, Kutacane, Kutoarjo, Labuhan, Lahat, Lamongan, Langsa, Larantuka, Lawang, Lhoseumawe, Limboto, Lubuk Basung, Lubuk Linggau, Lubuk Pakam, Lubuk Sikaping, Lumajang, Luwuk, Madiun, Magelang, Magetan, Majalengka, Majene, Makale, Makassar, Malang, Mamuju, Manna, Manokwari, Marabahan, Maros, Martapura Kalsel, Sulsel, Masohi, Mataram, Maumere, Medan, Mempawah, Menado, Mentok, Merauke, Metro, Meulaboh, Mojokerto, Muara Bulian, Muara Bungo, Muara Enim, Muara Teweh, Muaro Sijunjung, Muntilan, Nabire,Negara, Nganjuk, Ngawi, Nunukan, Pacitan, Padang, Padang Panjang, Padang Sidempuan, Pagaralam, Painan, Palangkaraya, Palembang, Palopo, Palu, Pamekasan, Pandeglang, Pangka_, Pangkajene Sidenreng, Pangkalan Bun, Pangkalpinang, Panyabungan, Par_, Parepare, Pariaman, Pasuruan, Pati, Payakumbuh, Pekalongan, Pekan Baru, Pemalang, Pematangsiantar, Pendopo, Pinrang, Pleihari, Polewali, Pondok Gede, Ponorogo, Pontianak, Poso, Prabumulih, Praya, Probolinggo, Purbalingga, Purukcahu, Purwakarta, Purwodadigrobogan, Purwarta Purworejo, Putussibau, Raha, Rangkasbitung, Rantau, Rantauprapat, Rantepao, Rembang, Rengat, Ruteng, Sabang, Salatiga, Samarinda, Kalbar, Sampang, Sampit, Sanggau, Sawahlunto, Sekayu, Selong, Semarang, Sengkang, Serang, Serui, Sibolga, Sidikalang, Sidoarjo, Sigli, Singaparna, Singaraja, Singkawang, Sinjai, Sintang, Situbondo, Slawi,Sleman, Soasiu, Soe, Solo, Solok, Soreang, Sorong, Sragen, Stabat, Subang, Sukabumi, Sukoharjo, Sumbawa Besar, Sumedang, Sumenep, Sungai Liat, Sungai Penuh, Sungguminasa, Surabaya, Surakarta, Tabanan, Tahuna, Takalar, Takengon , Tamiang Layang, Tanah Grogot, Tangerang, Tanjung Balai, Tanjung Enim, Tanjung Pandan, Tanjung Pinang, Tanjung Redep, Tanjung Selor, Tapak Tuan, Tarakan, Tarutung, Tasikmalaya, Tebing Tinggi, Tegal, Temanggung, Tembilahan, Tenggarong, Ternate, Tolitoli , Tondano, Trenggalek, Tual, Tuban, Tulung Agung, Ujung Berung, Ungaran, Waikabubak, Waingapu, Wamena, Watampone, Watansoppeng, Wates, Wonogiri, Wonosari, Wonosobo, YogyakartaTakalar, Takengon, Tamiang Layang, Tanah Grogot, Tangerang, Tanjung Balai, Tanjung Enim, Tanjung Pandan, Tanjung Pinang, Tanjung Redep, Tanjung Selor, Tapak Tuan, Tarakan, Tarutung, Tasikmalaya, Tebing Tinggi, Tegal, Temanggung, Tembilahan, Tenggarong, Ternate, Tolitoli, Tondano, Trenggalek, Tual, Tuban, Tulung Agung, Ujung Berung, Ungaran, Waikabubak, Waingapu, Wamena, Watampone, Watansoppeng, Wates, Wonogiri, Wonosari, Wonosobo, YogyakartaTakalar, Takengon, Tamiang Layang, Tanah Grogot, Tangerang, Tanjung Balai, Tanjung Enim, Tanjung Pandan, Tanjung Pinang, Tanjung Redep, Tanjung Selor, Tapak Tuan, Tarakan, Tarutung, Tasikmalaya, Tebing Tinggi, Tegal, Temanggung, Tembilahan, Tenggarong, Ternate, Tolitoli, Tondano, Trenggalek, Tual, Tuban, Tulung Agung, Ujung Berung, Ungaran, Waikabubak, Waingapu, Wamena, Watampone, Watansoppeng, Wates, Wonogiri, Wonosari, Wonosobo, YogyakartaWonogiri, Wonosari, Wonosobo, YogyakartaWonogiri, Wonosari, Wonosobo, Yogyakarta'
	no = 1
	hasil = ''
	for i in daerah.split(','):
		hasil += '%s. %s\n' % (no, i)
		no += 1
	return {
		'status': 200,
		'result': hasil
	}

@app.route('/api/jadwalshalat', methods=['GET','POST'])
def jadwalshalat():
	if request.args.get('daerah'):
		try:
			daer = request.args.get('daerah')
			daerah = 'Ambarawa, Ambon, Amlapura, Amuntai, Argamakmur, Atambua, Babo, Bagan Siapiapi, Kalteng, Bajawa, Balige, Balikpapan, Banda Aceh, Bandarlampung, Bandung, Bangkalan, Bangkinang, Bangko, Bangli, Banjar, Banjar Baru, Banjarmasin, Banjarnegara, Bantaeng, Banten, Bantul, Banyuwangi, Barabai, Barito, Barru, Batam, Batang, Batu, Baturaja, Batusangkar, Baubau, Bekasi, Bengkalis, Bengkulu, Benteng, Biak, Bima, Binjai, Bireuen, Bitung, Blitar, Blora, Bogor, Bojonegoro, Bondowoso, Bontang, Boyolali, Brebes, Bukit Tinggi, Maluku, Bulukumba, Buntok, Cepu, Ciamis, Cianjur, Cibinong, Cilacap, Cilegon, Cimahi, Cirebon, Curup, Demak, Denpasar, Depok, Dili, Dompu, Donggala, Dumai, Ende, Enggano, Enrekang, Fakfak, Garut, Gianyar, Gombong, Gorontalo, Gresik, Gunung Sitoli, Indramayu, Jakarta Barat, Jakarta Pusat, Jakarta Selatan, Jakarta Timur, Jakarta Utara, Jambi, Jayapura, Jember, Jeneponto, Jepara, Jombang, Kabanjahe, Kalabahi, Kalianda, Kandangan, Karanganyar, Karawang, Kasungan, Kayuagung, Kebumen, Kediri, Kefamenanu, Kendal, Kendari, Kertosono, Ketapang, Kisaran, Klaten, Kolaka, Kota Baru Pulau Laut, Kota Bumi, Kota Jantho, Kotamobagu, Kuala Kapuas, Kuala Kurun, Kuala Pembuang, Kuala Tungkal, Kudus, Kuningan, Kupang, Kutacane, Kutoarjo, Labuhan, Lahat, Lamongan, Langsa, Larantuka, Lawang, Lhoseumawe, Limboto, Lubuk Basung, Lubuk Linggau, Lubuk Pakam, Lubuk Sikaping, Lumajang, Luwuk, Madiun, Magelang, Magetan, Majalengka, Majene, Makale, Makassar, Malang, Mamuju, Manna, Manokwari, Marabahan, Maros, Martapura Kalsel, Sulsel, Masohi, Mataram, Maumere, Medan, Mempawah, Menado, Mentok, Merauke, Metro, Meulaboh, Mojokerto, Muara Bulian, Muara Bungo, Muara Enim, Muara Teweh, Muaro Sijunjung, Muntilan, Nabire, Negara, Nganjuk, Ngawi, Nunukan, Pacitan, Padang, Padang Panjang, Padang Sidempuan, Pagaralam, Painan, Palangkaraya, Palembang, Palopo, Palu, Pamekasan, Pandeglang, Pangka_, Pangkajene Sidenreng, Pangkalan Bun, Pangkalpinang, Panyabungan, Par_, Parepare, Pariaman, Pasuruan, Pati, Payakumbuh, Pekalongan, Pekan Baru, Pemalang, Pematangsiantar, Pendopo, Pinrang, Pleihari, Polewali, Pondok Gede, Ponorogo, Pontianak, Poso, Prabumulih, Praya, Probolinggo, Purbalingga, Purukcahu, Purwakarta, Purwodadigrobogan, Purwokerto, Purworejo, Putussibau, Raha, Rangkasbitung, Rantau, Rantauprapat, Rantepao, Rembang, Rengat, Ruteng, Sabang, Salatiga, Samarinda, Kalbar, Sampang, Sampit, Sanggau, Sawahlunto, Sekayu, Selong, Semarang, Sengkang, Serang, Serui, Sibolga, Sidikalang, Sidoarjo, Sigli, Singaparna, Singaraja, Singkawang, Sinjai, Sintang, Situbondo, Slawi, Sleman, Soasiu, Soe, Solo, Solok, Soreang, Sorong, Sragen, Stabat, Subang, Sukabumi, Sukoharjo, Sumbawa Besar, Sumedang, Sumenep, Sungai Liat, Sungai Penuh, Sungguminasa, Surabaya, Surakarta, Tabanan, Tahuna, Takalar, Takengon, Tamiang Layang, Tanah Grogot, Tangerang, Tanjung Balai, Tanjung Enim, Tanjung Pandan, Tanjung Pinang, Tanjung Redep, Tanjung Selor, Tapak Tuan, Tarakan, Tarutung, Tasikmalaya, Tebing Tinggi, Tegal, Temanggung, Tembilahan, Tenggarong, Ternate, Tolitoli, Tondano, Trenggalek, Tual, Tuban, Tulung Agung, Ujung Berung, Ungaran, Waikabubak, Waingapu, Wamena, Watampone, Watansoppeng, Wates, Wonogiri, Wonosari, Wonosobo, Yogyakarta'
			url = f'https://api.haipbis.xyz/jadwalsholat?daerah={daer}'
			jadwal = get(url).json()
			return {
				'Imsyak': jadwal['Imsyak'],
				'Subuh': jadwal['Subuh'],
				'Dhuha': jadwal['Dhuha'],
				'Dzuhur': jadwal['Dzuhur'],
				'Ashar': jadwal['Ashar'],
				'Maghrib': jadwal['Maghrib'],
				'Isya': jadwal['Isya']
			}
		except:
			return {
				'status': False,
				'error': '[❗] Daerah yang tersedia hanya : %s' % daerah
			}
	else:
		return {
			'status': False,
			'pesan': '[!] Masukkan parameter daerah'
		}

@app.route('/api/waifu', methods=['GET','POST'])
def waifu():
	scrap = bs(get('https://mywaifulist.moe/random').text, 'html.parser')
	a = json.loads(scrap.find('script', attrs={'type':'application/ld+json'}).string)
	desc = bs(get(a['url']).text, 'html.parser').find('meta', attrs={'property':'og:description'}).attrs['content']
	result = json.loads(bs(get(a['url']).text, 'html.parser').find('script', attrs={'type':'application/ld+json'}).string)
	if result['gender'] == 'female':
		return {
			'status': 200,
			'name': result['name'],
			'desc': desc,
			'image': result['image'],
			'source': result['url']
		}
	else:
		return {
			'status': 200,
			'name': '%s (husbu)' % result['name'],
			'desc': desc,
			'image': result['image'],
			'source': result['url']
		}

@app.route('/api/infogempa', methods=['GET','POST'])
def infogempa():
	be = bs(get('https://www.bmkg.go.id/').text, 'html.parser').find('div', class_="col-md-4 md-margin-bottom-10")
	em = be.findAll('li')
	img = be.find('a')['href']
	return {
		'status': 200,
		'map': img,
		'waktu': em[0].text,
		'magnitude': em[1].text,
		'kedalaman': em[2].text,
		'koordinat': em[3].text,
		'lokasi': em[4].text,
		'potensi': em[5].text
	}

@app.route('/api/randomquotes', methods=['GET','POST'])
def quotes():
	quotes_file = json.loads(open('quotes.json').read())
	result = random.choice(quotes_file)
	print(result)
	return {
		'status': 200,
		'author': result['author'],
		'quotes': result['quotes']
	}

@app.route('/api/quotesnime/random', methods=['GET','POST'])
def quotesnimerandom():
	quotesnime = get('https://animechanapi.xyz/api/quotes/random').json()['data'][0]
	return {
		'status': 200,
		'data': {
			'quote': quotesnime['quote'],
			'character': quotesnime['character'],
			'anime': quotesnime['anime']
		}
	}


@app.route('/api', methods=['GET','POST'])
def api():
	return render_template('api.html')

@app.route('/', methods=['GET','POST'])
def index():
	return render_template('index.html')

@app.errorhandler(404)
def error(e):
	return render_template('404.html'), 404
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=int(os.environ.get('PORT','5000')),debug=True)
