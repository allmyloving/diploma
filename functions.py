from data import db_utils
from data import twitter
from data.date_utils import *
from language_detection import language_detection


def load_test_data(lang, amount):
    if len(retrieve_test_data(lang)) > 0:
        raise Exception('Please load all data in one call')
    messages = twitter.get_tweets(amount, lang, since=minus_days(today(), 3))
    db_utils.store_test_data(messages, lang)


def load_train_data(lang, amount):
    if len(retrieve_train_data(lang)) > 0:
        raise Exception('Please load all data in one call')
    messages = twitter.get_tweets(amount, lang, until=minus_days(today(), 3))
    db_utils.store_train_data(messages, lang)


def retrieve_train_data(lang):
    return db_utils.retrieve_train_data_by_language(lang)


def retrieve_test_data(lang):
    return db_utils.retrieve_test_data_by_language(lang)


def cleanup_all_data():
    db_utils.cleanup()


def detect_language(message, classifier='naive_bayes', train_data_amount=50):
    language_detection.train(classifier, train_data_amount)
    return language_detection.predict(message)
