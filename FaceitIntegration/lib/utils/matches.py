def is_won_match(player_id, match):
    winner_faction = match["results"]["winner"]
    player_faction = "faction2"
    faction_to_check = "faction1"

    for player in match["teams"][faction_to_check]["players"]:
        player_faction = faction_to_check if player["player_id"] == player_id else player_faction

    return winner_faction == player_faction


def get_match_id(match):
    return match['match_id']


def is_matchmaking(match):
    return match["competition_type"] == "matchmaking"
