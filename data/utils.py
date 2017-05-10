import sqlite3
from data import constants
from datetime import date
from datetime import timedelta
import os


def count_symbols(lang):
    total_len = 0
    text_lang_folder = os.path.join(constants.WIKIPEDIA_TEXT_FOLDER, lang)
    for file in os.listdir(text_lang_folder):
        total_len += len(open(os.path.join(text_lang_folder, file), encoding='utf-8').read())
    return total_len


def tomorrow():
    return today() + timedelta(days=1)


def today():
    return date.today()


def plus_days(date, days):
    return date + timedelta(days)


def minus_days(date, days):
    return date - timedelta(days)


def store_data(table_name, messages, lang):
    conn = sqlite3.connect(constants.DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS %s
                 (data text unique, lang text)''' % table_name)
    for message in messages:
        cursor.execute("select * from %s where data=?" % table_name, (message,))
        if not cursor.fetchone():
            cursor.execute("insert into %s values (?, ?)" % table_name, (message, lang))
        conn.commit()
    conn.close()


def store_test_data(messages, lang):
    store_data('test_set', messages, lang)


def store_train_data(messages, lang):
    store_data('train_set', messages, lang)
