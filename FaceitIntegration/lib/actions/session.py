import codecs
import json
import os
import time
from datetime import datetime

from ..utils.matches import is_won_match, get_match_id, is_matchmaking
from ..FaceitApi import get_player_matches
from .elo import get_player_info

DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', '..', 'settings')
DATA_FILE = os.path.join(DATA_DIRECTORY, 'session.json')


def init_session(parent, arguments):
    player_info = get_player_info(parent, arguments)

    session_data = {
        'init': int(time.mktime(datetime.now().timetuple())),
        'player_id': player_info['player_id'],
        'elo': player_info['elo'],
        # TODO: Remove this when FACEIT API gets FIXED
        'initial_matches': set_initial_matches_deprecated(parent, arguments['api_key'], player_info['player_id'])
    }

    with codecs.open(DATA_FILE, encoding='utf-8-sig', mode='w+') as f:
        json.dump(session_data, f, encoding='utf-8', ensure_ascii=False)
    with codecs.open(DATA_FILE.replace('.json', '.js'), encoding='utf-8-sig', mode='w+') as f:
        f.write(
            'const settings = {0};'.format(json.dumps(session_data, f, encoding='utf-8', ensure_ascii=False)))

    if arguments['overlays_enabled']:
        parent.BroadcastWsEvent('EVENT_FCARRASCOSA_FACEIT_SESSION_START', '')


def get_session_initial_data():
    with codecs.open(DATA_FILE, encoding='utf-8-sig', mode='r') as f:
        session_data = json.load(f, encoding='utf-8-sig')

    return session_data


def get_session_analysis(parent, arguments):
    api_key = arguments['api_key']
    initial_data = get_session_initial_data()
    initial_date = initial_data['init']
    initial_elo = initial_data['elo']
    player_id = initial_data['player_id']
    get_all = arguments['include_all_matches']
    current_elo = get_player_info(parent, arguments)['elo']

    matches = [match for match in get_player_matches(parent, api_key, player_id, matches_from=initial_date)["items"] if
               (get_all or is_matchmaking(match))]
    won_matches = 0
    total_matches = len(matches)

    for match in matches:
        won_matches += 1 if is_won_match(player_id, match) else 0

    result = {
        'total_matches': total_matches,
        'won_matches': won_matches,
        'lost_matches': total_matches - won_matches,
        'elo_balance': current_elo - initial_elo,
    }

    if arguments['overlays_enabled']:
        parent.BroadcastWsEvent('EVENT_FCARRASCOSA_FACEIT_SESSION_UPDATE', json.dumps(result))

    return result


# TODO: Remove this when FACEIT API gets FIXED
def set_initial_matches_deprecated(parent, api_key, player_id):
    matches = get_player_matches(parent, api_key, player_id)["items"]

    return map(get_match_id, matches)


# TODO: Remove this when FACEIT API gets FIXED
def get_session_analysis_deprecated(parent, arguments):
    api_key = arguments['api_key']
    get_all = arguments['include_all_matches']
    initial_data = get_session_initial_data()
    initial_elo = initial_data['elo']
    initial_matches = initial_data['initial_matches']
    player_id = initial_data['player_id']
    current_elo = get_player_info(parent, arguments)['elo']

    matches = get_player_matches(parent, api_key, player_id)["items"]
    matches_to_analyze = []
    won_matches = 0

    for match in matches:
        if match['match_id'] not in initial_matches and (get_all or is_matchmaking(match)):
            matches_to_analyze.append(match)

    total_matches = len(matches_to_analyze)

    for match in matches_to_analyze:
        won_matches += 1 if is_won_match(player_id, match) else 0

    result = {
        'total_matches': total_matches,
        'won_matches': won_matches,
        'lost_matches': total_matches - won_matches,
        'elo_balance': current_elo - initial_elo,
    }

    if arguments['overlays_enabled']:
        parent.BroadcastWsEvent('EVENT_FCARRASCOSA_FACEIT_SESSION_UPDATE', json.dumps(result))

    return result
