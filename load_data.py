import requests

HOST = 'api.twitter.com'
AUTH_PATH = '/oauth2/token'
SEARCH_PATH = '/1.1/search/tweets.json'
ACCESS_TOKEN_PARAM = 'access_token'
GRANT_TYPE_PARAM = 'grant_type'
CLIENT_CREDENTIALS = 'client_credentials'

CONSUMER_KEY = 'I7IzOl39eH1KqXaUGzw1TlfeU'
CONSUMER_SECRET = 'e1I2lEbyDVnpJe8JOawYx78DIh9WdhU6SeFHtMVvYbjKH8AA62'


def get_token():
    token_params = {
        GRANT_TYPE_PARAM: CLIENT_CREDENTIALS
    }
    url = 'https://' + HOST + AUTH_PATH
    response = requests.post(url, token_params, auth=(CONSUMER_KEY, CONSUMER_SECRET))
    if response.status_code != 200:
        print('Request unsuccessful, response code: %d' % response.status_code)
    else:
        return response.json().get('access_token')


def search(token, q, lang='en'):
    search_params = {
        'q': q,
        'lang': lang
    }
    url = 'https://' + HOST + SEARCH_PATH
    headers = {
        'Authorization': 'Bearer '.join(token),
        'Accept-Encoding': 'gzip'
    }
    response = requests.get(url, search_params, headers=headers)
    if response.status_code != 200:
        print('Request unsuccessful, response code: %d' % response.status_code)
    return response.json()


token = get_token()
results = search(token, 'nasa')
print(results)
