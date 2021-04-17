from ..FaceitApi import get_player


def get_player_info(parent, arguments):
    player = arguments['argument'] if arguments['argument'] else arguments['default_player']
    api_key = arguments['api_key']
    player_info = get_player(parent, api_key, player)

    return {
        'elo': player_info['games']['csgo']['faceit_elo'],
        'level': player_info['games']['csgo']['skill_level'],
        'player_id': player_info['player_id'],
        'player': player
    }
