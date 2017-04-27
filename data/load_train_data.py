import requests
from data import constants
import os
import lxml.html
from lxml.etree import ElementTree

pages = {
    u'ru': 'http://ru.wikipedia.org/wiki/%D0%92%D0%B8%D0%BA%D0%B8%D0%BF%D0%B5%D0%B4%D0%B8%D1%8F',
    u'uk': 'https://uk.wikipedia.org/wiki/%D0%92%D1%96%D0%BA%D1%96%D0%BF%D0%B5%D0%B4%D1%96%D1%8F',
    u'sr': 'https://sr.wikipedia.org/wiki/%D0%92%D0%B8%D0%BA%D0%B8%D0%BF%D0%B5%D0%B4%D0%B8%D1%98%D0%B0',
}


def create_folder_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def save_to_file(filename, content):
    print("Writing %s" % filename)
    open(filename, 'wb').write(content.encode('utf-8', 'ignore'))


def get_dom_tree(page):
    html_content = requests.get(page, headers=headers).content
    return ElementTree(lxml.html.document_fromstring(html_content))


def compose_filename(text_lang_folder, lang, num):
    return os.path.join(text_lang_folder, '%s_%04d.txt' % (lang, num))


headers = {
    'User-Agent': 'OpenAnything/1.0'
}
for lang, page in pages.items():
    text_lang_folder = os.path.join(constants.WIKIPEDIA_TEXT_FOLDER, lang)
    create_folder_if_not_exists(text_lang_folder)

    tree = get_dom_tree(page)
    i = 0
    for p in tree.findall('//p'):
        content = p.text_content()
        if len(content) > constants.MINIMUM_PARAGRAPH_LENGTH:
            save_to_file(compose_filename(text_lang_folder, lang, i), content)
            i += 1
