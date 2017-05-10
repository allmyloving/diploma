import requests
import lxml.html
from lxml.etree import ElementTree

pages = {
    u'ru': 'https://ru.wikipedia.org/wiki/%D0%AF%D0%B7%D1%8B%D0%BA',
    u'uk': 'https://uk.wikipedia.org/wiki/%D0%9C%D0%BE%D0%B2%D0%B0',
    u'sr': 'https://sr.wikipedia.org/wiki/%D0%92%D0%B8%D0%BA%D0%B8%D0%BF%D0%B5%D0%B4%D0%B8%D1%98%D0%B0',
}

headers = {
    'User-Agent': 'OpenAnything/1.0'
}


def get_dom_tree(page):
    html_content = requests.get(page, headers=headers).content
    return ElementTree(lxml.html.document_fromstring(html_content))


def download_wiki(lang):
    tree = get_dom_tree(pages[lang])

    messages = []
    for p in tree.findall('//p'):
        content = p.text_content()
        [messages.extend(m) for m in content.split('.')]
    return messages
