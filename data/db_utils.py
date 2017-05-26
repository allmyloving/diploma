import sqlite3
from data import constants
import sys


def __store_data(table_name, messages, lang):
    conn = sqlite3.connect(constants.DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS %s
                 (data text unique, lang text)''' % table_name)
    for message in messages:
        cursor.execute("insert into %s values (?, ?)" % table_name, (message, lang))
    conn.commit()
    cursor.close()
    conn.close()


def store_test_data(messages, lang):
    __store_data(constants.TEST_SET_DB_TABLE_NAME, messages, lang)


def store_train_data(messages, lang):
    __store_data(constants.TRAIN_SET_DB_TABLE_NAME, messages, lang)


def __get_all_languages(table_name):
    conn = sqlite3.connect(constants.DB_NAME)
    cursor = conn.cursor()
    cursor.execute('select DISTINCT lang from %s' % table_name)
    result = list(cursor)
    cursor.close()
    conn.close()
    return [x for y in result for x in y]


def __retrieve_data_for_all_languages(table_name, amount_for_lang=sys.maxsize):
    languages = __get_all_languages(table_name)
    total = []
    for lang in languages:
        data = __retrieve_data(table_name, lang, amount_for_lang)
        if len(data) < amount_for_lang:
            raise Exception(
                "Not enough data loaded. Required: %d, found: %d (lang %s)" % (amount_for_lang, len(data), lang))
        total.extend(data)
    return total


def __retrieve_data(table_name, lang, amount=sys.maxsize):
    conn = sqlite3.connect(constants.DB_NAME)
    cursor = conn.cursor()
    cursor.execute('select * from %s where lang=? limit ?' % table_name, (str(lang), str(amount)))
    result = list(cursor)
    cursor.close()
    conn.close()
    return result


def retrieve_train_data(amount_for_lang):
    return __retrieve_data_for_all_languages(constants.TRAIN_SET_DB_TABLE_NAME, amount_for_lang)


def retrieve_train_data_by_language(lang):
    return __retrieve_data(constants.TRAIN_SET_DB_TABLE_NAME, lang)


def retrieve_test_data_by_language(lang):
    return __retrieve_data(constants.TEST_SET_DB_TABLE_NAME, lang)


def retrieve_test_data(amount_for_lang):
    return __retrieve_data_for_all_languages(constants.TEST_SET_DB_TABLE_NAME, amount_for_lang)


def __cleanup_table(table_name):
    conn = sqlite3.connect(constants.DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='%s'" % table_name)
    if cursor.fetchone() is not None:
        cursor.execute('DELETE FROM %s' % table_name)
        conn.commit()
    cursor.close()
    conn.close()


def cleanup():
    __cleanup_table(constants.TRAIN_SET_DB_TABLE_NAME)
    __cleanup_table(constants.TEST_SET_DB_TABLE_NAME)
