from StringIO import StringIO
import os
import sys
import tempfile

from PIL import Image
import requests


card_number = sys.argv[1]
cpf = sys.argv[2]

session = requests.Session()

POST_URL = 'https://sodexosaldocartao.com.br/saldocartao/consultaSaldo.do?operation=consult'
CAPTCHA_URL = 'https://sodexosaldocartao.com.br/saldocartao/jcaptcha.do'

r = session.get(CAPTCHA_URL)
i = Image.open(StringIO(r.content))
i.show()

captcha_text = raw_input('CAPTCHA: ')

post_data = {
    'service': '5;1;6',
    'cardNumber': card_number,
    'cpf': cpf,
    'jcaptcha_response': captcha_text,
    'x': '6',
    'y': '9',
}

r = session.post(POST_URL, params=post_data)

f = tempfile.NamedTemporaryFile(delete=False)
f.write(r.content)
f.close()

os.system('google-chrome ' + f.name)
