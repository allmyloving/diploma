import sqlite3
import requests
from data import constants


def get_token():
    token_params = {
        constants.GRANT_TYPE_PARAM: constants.CLIENT_CREDENTIALS
    }
    url = 'https://' + constants.HOST + constants.AUTH_PATH
    response = requests.post(url, token_params, auth=(constants.CONSUMER_KEY, constants.CONSUMER_SECRET))
    if response.status_code != 200:
        print('Request unsuccessful, response code: %d' % response.status_code)
    else:
        return response.json().get('access_token')


def search(token, q, lang='en'):
    search_params = {
        'q': q,
        'lang': lang
    }
    url = 'https://' + constants.HOST + constants.SEARCH_PATH
    headers = {
        'Authorization': 'Bearer ' + token,
        'Accept-Encoding': 'gzip'
    }
    response = requests.get(url, search_params, headers=headers)
    return response.status_code, response.json()


def transform(json):
    tweets = list(json.get('statuses'))
    return [t.get('text') for t in tweets]


def store_tweets(tweets, lang):
    conn = sqlite3.connect('test_set.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tweet
             (data text unique, lang text)''')
    for tweet in tweets:
        cursor.execute("select * from tweet where data=?", (tweet,))
        if not cursor.fetchone():
            cursor.execute("insert into tweet values (?, ?)", (tweet, lang))
        conn.commit()
    conn.close()


token = get_token()
lang = 'en'
status_code, json = search(token, 'nasa', lang)
print(json)
if status_code == 200:
    tweets_text = transform(json)
    store_tweets(tweets_text, lang)
