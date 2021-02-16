import json

class FaceitApiClient:
    def __init__(self, apiKey="", parent=None):
        self.apiBaseUri = "https://open.faceit.com/data/v4/"
        self.apiKey = apiKey
        self.parent = parent

    def getPlayer(self, nickname):
        requestUrl = self.apiBaseUri + "players?nickname=" + nickname
        requestHeaders = {"Authorization": "Bearer " + self.apiKey}
        result = self.parent.GetRequest(requestUrl, requestHeaders)
        parsedResult = json.loads(result)
        return json.loads(parsedResult["response"])

    def getPlayerElo(self, nickname):
        playerInfo = self.getPlayer(nickname)
        return str(playerInfo["games"]["csgo"]["faceit_elo"])
