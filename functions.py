from data import twitter
from data import utils
import re


def load_test_data(amount, lang):
    messages = twitter.get_tweets(amount, lang, since=utils.minus_days(utils.today(), 3))
    utils.store_test_data(messages, lang)


def load_train_data(amount, lang):
    messages = twitter.get_tweets(amount, lang, until=utils.minus_days(utils.today(), 3))
    messages = remove_redundant_symbols(messages)
    utils.store_train_data(messages, lang)


def remove_redundant_symbols(messages):
    return [re.sub(r'(http|@)\S*', '', m) for m in messages]


def detect_language(message):
    pass




