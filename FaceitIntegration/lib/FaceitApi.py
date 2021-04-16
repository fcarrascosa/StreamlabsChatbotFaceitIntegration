import time
from datetime import datetime

from utils.requests import generate_query_string, make_get_request

FACEIT_API_BASE_URL = 'https://open.faceit.com/data/v4/'

FACEIT_API_ENDPOINTS = {
    'players': 'players',
    'players_matches': 'players/:player_id:/history'
}


def get_player(parent, api_key, nickname):
    params = {
        'nickname': nickname
    }

    request_url = FACEIT_API_BASE_URL + FACEIT_API_ENDPOINTS['players'] + generate_query_string(params)

    return make_get_request(parent, request_url, api_key)


def get_player_matches(parent, api_key, player_id, matches_from=None, matches_to=None, offset=0, limit=None):
    params = {
        'from': matches_from,
        'to': matches_to if matches_to else int(time.mktime(datetime.now().timetuple())),
        'offset': offset,
        'limit': limit
    }

    endpoint = FACEIT_API_ENDPOINTS['players_matches'].replace(':player_id:', player_id)
    request_url = FACEIT_API_BASE_URL + endpoint + generate_query_string(params)

    return make_get_request(parent, request_url, api_key)["items"]
