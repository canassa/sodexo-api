from StringIO import StringIO
import os
import sys
import tempfile

from bs4 import BeautifulSoup
from PIL import Image
import requests


POST_URL = 'https://sodexosaldocartao.com.br/saldocartao/consultaSaldo.do?operation=consult'
CAPTCHA_URL = 'https://sodexosaldocartao.com.br/saldocartao/jcaptcha.do'


def solve_captcha(image):
    pixel_data = image.load()

    for x in xrange(image.size[0]):
        for y in xrange(image.size[1]):
            pixel = pixel_data[x, y]
            if pixel[0] < 220 and pixel[1] < 220 and pixel[2] > 130:
                pixel_data[x, y] = (255, 255, 255)
            else:
                pixel_data[x, y] = (0, 0, 0)

    return image


def parse_html(html):
    soup = BeautifulSoup(html)

    errors = soup.find(class_='textRed')
    if errors:
        return errors.string.strip()


def get_captcha(session):
    r = session.get(CAPTCHA_URL)
    return Image.open(StringIO(r.content))


def post_card(session, card_number, cpf, captcha_text):
    post_data = {
        'service': '5;1;6',
        'cardNumber': card_number,
        'cpf': cpf,
        'jcaptcha_response': captcha_text,
        'x': '6',
        'y': '9',
    }

    r = session.post(POST_URL, params=post_data)

    return r.content


def get_balance(card_number, cpf):
    session = requests.Session()

    captcha_image = get_captcha(session)

    # TODO: Automate the captcha
    captcha_image.show()
    captcha_text = raw_input("CAPTCHA:")

    return parse_html(post_card(session, card_number, cpf, captcha_text))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print >> sys.stderr, 'usage: ' + sys.argv[0] + ' card_number cpf'
        sys.exit(1)

    print get_balance(*sys.argv[1:])
