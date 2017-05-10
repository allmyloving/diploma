import sqlite3
from data import constants
from datetime import date
from datetime import timedelta


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
