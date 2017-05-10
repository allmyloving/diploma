import requests
from data import constants
import sqlite3
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


def store(conn, text, lang):
    cursor = conn.cursor()
    cursor.execute("select * from train_set where data=?", (text,))
    if not cursor.fetchone():
        cursor.execute("insert into train_set values (?, ?)", (text, lang))
    conn.commit()


def store_all():
    for lang, page in pages.items():
        tree = get_dom_tree(page)
        conn = sqlite3.connect(constants.DB_NAME)
        conn.cursor().execute('''CREATE TABLE IF NOT EXISTS train_set
                 (data text unique, lang text)''')

        for p in tree.findall('//p'):
            content = p.text_content()
            [store(conn, s, lang) for s in content.split('.')]


store_all()
