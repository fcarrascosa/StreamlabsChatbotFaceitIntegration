import codecs
import os

from ..FaceitApi import get_player


def get_player_info(parent, arguments):
    player = arguments['argument'] if ('argument' in arguments.keys() and arguments['argument']) else arguments[
        'default_player']
    api_key = arguments['api_key']
    player_info = get_player(parent, api_key, player)

    return {
        'elo': player_info['games']['csgo']['faceit_elo'],
        'level': player_info['games']['csgo']['skill_level'],
        'player_id': player_info['player_id'],
        'player': player
    }


def get_player_elo_overlay(parent, arguments):
    data_directory = os.path.join(os.path.dirname(__file__), '..', '..', 'overlays', 'text')
    data_file = os.path.join(data_directory, 'elo.txt')

    elo = get_player_info(parent, arguments)['elo']
    with codecs.open(data_file, encoding='utf-8-sig', mode='w+') as f:
        f.write(
            '{0}'.format(elo))
