import requests
from data import constants
from data import utils


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


def search(token, q, lang, since='2017-01-01', until=utils.tomorrow(), count='100', max_id=''):
    search_params = {
        'q': q,
        'lang': lang,
        'count': count,
        'max_id': max_id,
        'since': since,
        'until': until,
        'include_entities': False
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
    return [t.get('text') for t in tweets], min([t.get('id') for t in tweets])
