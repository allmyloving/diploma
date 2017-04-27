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

text_folder = u'paragraphs'

headers = {
    'User-Agent': 'OpenAnything/1.0'
}
for lang, page in pages.items():
    text_lang_folder = os.path.join(text_folder, lang)
    if not os.path.exists(text_lang_folder):
        os.makedirs(text_lang_folder)
    html_content = requests.get(page, headers=headers).content
    tree = ElementTree(lxml.html.document_fromstring(html_content))
    i = 0
    j = 0
    for p in tree.findall('//p'):
        content = p.text_content()
        if len(content) < 100:
            continue

        text_filename = os.path.join(text_lang_folder,
                                     '%s_%04d.txt' % (lang, i))
        print("Writing %s" % text_filename)
        open(text_filename, 'wb').write(content.encode('utf-8', 'ignore'))
        i += 1
