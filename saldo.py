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

pixel_data = i.load()

for x in xrange(i.size[0]):
    for y in xrange(i.size[1]):
        pixel = pixel_data[x, y]
        if pixel[0] < 220 and pixel[1] < 220 and pixel[2] > 130:
            pixel_data[x, y] = (255, 255, 255)
        else:
            pixel_data[x, y] = (0, 0, 0)

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
