import time
import datetime

class FaceitSessionAnalyzer:
    def __init__(self, nick_name, get_all=False, parent=None):
        self.session_init = None
        self.nick_name = nick_name
        self.get_all = get_all
        self.matches = []
        self.initial_elo = 0
        self.initial_matches = []

    def start_session(self, initial_elo, matches):
        self.session_init = int(time.mktime(datetime.datetime.now().timetuple()))
        self.initial_elo = initial_elo

        matches_to_init = matches
        if not self.get_all:
            matches_to_init = [match for match in matches if match["competition_type"] == "matchmaking"]
        self.initial_matches = matches_to_init

    def set_matches(self, matches):

        matches = [match for match in matches if match not in self.initial_matches]

        if not self.get_all:
            matches = [match for match in matches if
                       match["competition_type"] == "matchmaking"]
        self.matches = matches

    def is_won_match(self, match=None):
        player_faction = None
        winner_faction = match["results"]["winner"]

        for key, value in match["teams"].items():
            for player in value["players"]:
                player_faction = key if player["nickname"] == self.nick_name else player_faction

        return player_faction == winner_faction

    def count_won_matches(self):
        value = 0

        for match in self.matches:
            value += 1 if self.is_won_match(match) else 0

        return value

    def count_total_matches(self):
        return len(self.matches)

    def count_lost_matches(self):
        return self.count_total_matches() - self.count_won_matches()

    def get_session_elo(self, current_elo):
        return current_elo - self.initial_elo
