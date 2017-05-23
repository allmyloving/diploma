from data import twitter
from data import db_utils
from data.date_utils import *
import re
from language_detection import language_detection


def load_test_data(lang, amount):
    messages = twitter.get_tweets(amount, lang, since=minus_days(today(), 3))
    db_utils.store_test_data(messages, lang)


def load_train_data(lang, amount):
    messages = twitter.get_tweets(amount, lang, until=minus_days(today(), 3))
    messages = remove_redundant_symbols(messages)
    db_utils.store_train_data(messages, lang)


def remove_redundant_symbols(messages):
    return [re.sub(r'(http|@)\S*', '', m) for m in messages if len(m) > 20]


def retrieve_train_data(lang):
    return db_utils.retrieve_train_data_by_language(lang)


def retrieve_test_data(lang):
    return db_utils.retrieve_test_data_by_language(lang)


def detect_language(message, train_data_amount=50):
    language_detection.train('svm', train_data_amount)
    return language_detection.predict(message)
