import sqlite3
from data import constants
from datetime import date
from datetime import timedelta
import sys


def tomorrow():
    return today() + timedelta(days=1)


def today():
    return date.today()


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
    store_data(constants.TEST_SET_DB_TABLE_NAME, messages, lang)


def store_train_data(messages, lang):
    store_data(constants.TRAIN_SET_DB_TABLE_NAME, messages, lang)


def get_all_languages(table_name):
    conn = sqlite3.connect(constants.DB_NAME)
    cursor = conn.cursor()
    cursor.execute('select DISTINCT lang from %s' % table_name)
    return [x for y in list(cursor) for x in y]


def retrieve_data_for_all_languages(table_name, amount_for_lang=sys.maxsize):
    languages = get_all_languages(table_name)
    total = []
    for lang in languages:
        data = retrieve_data(table_name, lang, amount_for_lang)
        if len(data) < amount_for_lang:
            raise Exception(
                "Not enough data loaded. Required: %d, found: %d (lang %s)" % (amount_for_lang, len(data), lang))
        total.extend(data)
    return total


def retrieve_data(table_name, lang, amount=sys.maxsize):
    conn = sqlite3.connect(constants.DB_NAME)
    cursor = conn.cursor()
    cursor.execute('select * from %s where lang=? limit ?' % table_name, (str(lang), str(amount)))
    return list(cursor)


def retrieve_train_data(amount_for_lang):
    return retrieve_data_for_all_languages(constants.TRAIN_SET_DB_TABLE_NAME, amount_for_lang)


def retrieve_train_data_by_language(lang):
    return retrieve_data(constants.TRAIN_SET_DB_TABLE_NAME, lang)


def retrieve_test_data(amount_for_lang):
    return retrieve_data_for_all_languages(constants.TEST_SET_DB_TABLE_NAME, amount_for_lang)
