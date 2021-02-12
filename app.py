from flask import *
from lib.nulis import *
from requests import get, post
from bs4 import BeautifulSoup as bs
import os, math, json, random, re, base64, time, smtplib

app = Flask(__name__)
app.config['MEDIA'] = 'private'


def convert_size(size_bytes):
	if size_bytes == 0:
		return '0B'
	size_name = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
	i = int(math.floor(math.log(size_bytes, 1024)))
	p = math.pow(1024, i)
	s = round(size_bytes / p, 2)
	return '%s %s' % (s, size_name[i])

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

@app.route('/api/statuscode', methods=['GET','POST'])
def statuscode():
	if request.args.get('code'):
		try:
			code = int(request.args.get('code'))
			return { 'status': 200, 'result': HTTP_STATUS_CODES[code] }
		except Exception as e:
			return { 'status': 200, 'result': 'Tidak Ada Code Respon'}
	else:
		return { 'status': False, 'pesan': 'Masukkan parameter code'}
	
@app.route('/api/rncode', methods=['GET','POST'])
def randomc_nhentai_code():
	return 'Random'

@app.route('/sendimage/<path:filename>', methods=['GET','POST'])
def sendimage(filename):
	return '`data:image/jpg;base64,%s`' % open(filename).read()

@app.route('/private/<path:filename>', methods=['GET','POST'])
def sendprivate(filename):
	return send_from_directory(app.config['MEDIA'], filename, as_attachment=True)

@app.route('/api/hili', methods=['GET','POST'])
def hili():
	if request.args.get('text'):
		text = str(request.args.get('text'))
		result = text.replace('a', 'i').replace('A', 'I').replace('u', 'i').replace('U', 'I').replace('e', 'i').replace('E', 'I').replace('o', 'i').replace('O', 'I')
		return { 'status': 200, 'result': result }
	else:
		return { 'status': False, 'pesan': 'Masukkan parameter number'}

@app.route('/api/convertsize', methods=['GET','POST'])
def hitung():
	if request.args.get('number'):
		try:
			number = int(request.args.get('number'))
			if number > 9999999999999999999999999999:
				return { 'status': 200, 'result': 'Nominal Terlalu Banyak' }
			else:
				result = convert_size(number)
				return { 'status': 200, 'result': result }
		except Exception as e:
			print(e)
			return { 'status': False, 'pesan': 'Harus Berupa Angka'}
	else:
		return { 'status': False, 'pesan': 'Masukkan parameter number'}

@app.route('/api/pinterest', methods=['GET','POST'])
def pinterest():
	if request.args.get('q'):
		q = request.args.get('q')
		pinterest_url = f'https://api.fdci.se/rep.php?gambar={q}'
		pin = get(pinterest_url).json()
		result = random.choice(pin)
		return { 'status': 200, 'result': result }
	else:
		return { 'status': False, 'pesan': 'Masukkan parameter q'}


@app.route('/api/randomquotes', methods=['GET','POST'])
def randomquotes():
	quotes_file = json.loads(open('quotes.json').read())
	result = random.choice(quotes_file)
	return { 'status': 200, 'result': result }

@app.route('/api/husbu', methods=['GET','POST'])
def husbu():
	husbu_file = json.loads(open('husbu.json').read())
	result = random.choice(husbu_file)
	return { 'status': 200, 'result': result }

@app.route('/api/simi', methods=['GET','POST'])
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

@app.route('/api/hartatahta', methods=['GET','POST'])
def hartatahta():
	if request.args.get('text'):
			tahta_txt = request.args.get('text')
			tahta_post = f'http://localhost:8080/test.php?text={tahta_txt}'
			tahta_hasil = get(tahta_post).json()
			return { 'status': 200, 'result': tahta_hasil['result'] }
	else:
		return { 'status': False, 'pesan': 'Masukkan parameter text'}
		

@app.route('/api/spamgmail', methods=['GET','POST'])
def spamgmail():
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
                server.login('fungame759@gmail.com', 'erlangga123')
                hasil = ''
                for i in range(jumlah):
                    mess = ''.join(random.choice(abece) for _ in range(4))
                    msg = f'From: {random.randint(1, 100)}<Hacker>\nSubject: Anonymous ~ Hacker\n{mess}'
                    server.sendmail('fungame759@gmail.com', target_imel, msg)
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

@app.route('/api', methods=['GET','POST'])
def api():
	return render_template('index.html')

@app.route('/', methods=['GET','POST'])
def home():
	return render_template('index.html')

@app.errorhandler(404)
def error(e):
	return render_template('404.html'), 404
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=int(os.environ.get('PORT','5000')),debug=True)


@app.errorhandler(500)
def error(e):
	print(e)
	return render_template('404.html'), 500
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=int(os.environ.get('PORT','5000')),debug=True)
