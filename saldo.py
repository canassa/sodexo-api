from StringIO import StringIO
import os
import sys
import tempfile

from bs4 import BeautifulSoup
from PIL import Image
import requests


POST_URL = 'https://sodexosaldocartao.com.br/saldocartao/consultaSaldo.do?operation=consult'
CAPTCHA_URL = 'https://sodexosaldocartao.com.br/saldocartao/jcaptcha.do'


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
