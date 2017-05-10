from data import load_tweets
from data import utils
import re


def get_data(amount, lang, since='2017-01-01', until=utils.tomorrow()):
    token = load_tweets.get_token()
    all_messages = []
    min_id = ''
    count = amount if amount < 100 else 100

    while len(all_messages) < amount:
        json = get_messages(lang, token, count, since, until, min_id)
        messages, min_id = load_tweets.transform(json)
        all_messages.extend(messages)
    return all_messages


def get_messages(lang, token, count, since, until, max_id):
    status_code, json = load_tweets.search(token, 'a', lang, since, until, count, max_id=max_id)
    if status_code != 200:
        raise Exception("Twitter is unavailable")
    return json


def load_test_data(amount, lang):
    messages = get_data(amount, lang, since=utils.minus_days(utils.today(), 3))
    utils.store_test_data(messages, lang)


def load_train_data(amount, lang):
    messages = get_data(amount, lang, until=utils.minus_days(utils.today(), 3))
    messages = remove_redundant_symbols(messages)
    utils.store_train_data(messages, lang)


def remove_redundant_symbols(messages):
    return [re.sub(r'[http|@()]\S*', '', m) for m in messages]
