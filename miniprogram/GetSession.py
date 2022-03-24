import requests


def get_session(url, params):
    return requests.get(url, params=params)
