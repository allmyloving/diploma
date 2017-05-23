from data import twitter
from data import utils
import re
from language_detection import language_detection


def load_test_data(lang, amount):
    messages = twitter.get_tweets(amount, lang, since=utils.minus_days(utils.today(), 3))
    utils.store_test_data(messages, lang)


def load_train_data(lang, amount):
    messages = twitter.get_tweets(amount, lang, until=utils.minus_days(utils.today(), 3))
    messages = remove_redundant_symbols(messages)
    utils.store_train_data(messages, lang)


def remove_redundant_symbols(messages):
    return [re.sub(r'(http|@)\S*', '', m) for m in messages if len(m) > 20]


def retrieve_train_data(lang):
    return utils.retrieve_train_data_by_language(lang)


def retrieve_test_data(lang):
    return utils.retrieve_test_data_by_language(lang)


def detect_language(message, train_data_amount=50):
    language_detection.train('svm', train_data_amount)
    return language_detection.predict(message)
