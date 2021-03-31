import json
import datetime
import time


class FaceitApiClient:
    def __init__(self, api_key="", parent=None):
        self.api_base_url = "https://open.faceit.com/data/v4/"
        self.api_key = api_key
        self.parent = parent

    def get_player(self, nick_name):
        request_url = self.api_base_url + "players?nickname=" + nick_name
        request_headers = {"Authorization": "Bearer " + self.api_key}
        result = self.parent.GetRequest(request_url, request_headers)
        parsed_result = json.loads(result)

        return json.loads(parsed_result["response"])

    def get_player_elo(self, nick_name):
        player_info = self.get_player(nick_name)
        return {
            "elo": player_info["games"]["csgo"]["faceit_elo"],
            "level": player_info["games"]["csgo"]["skill_level"]
        }

    def get_match_history(self, nick_name, get_from=None, get_to=None):
        player_info = self.get_player(nick_name)
        player_id = player_info["player_id"]
        request_url = self.api_base_url + "players/" + player_id + "/history?game=csgo"
        request_url = request_url + "&from=" + str(get_from) if get_from else request_url
        request_url = request_url + "&to=" + (str(get_to) if get_to else str(int(time.mktime(datetime.datetime.now().timetuple()))))
        request_url = request_url + "&limit=" + "100"
        request_headers = {"Authorization": "Bearer " + self.api_key}
        result = self.parent.GetRequest(request_url, request_headers)
        parsed_result = json.loads(result)["response"]
        return json.loads(parsed_result)["items"]
