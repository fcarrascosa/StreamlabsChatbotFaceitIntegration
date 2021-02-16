import os
import codecs
import json


class FaceitIntegrationSettings(object):
    def __init__(self, settingsfile=None):
        try:
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
                self.__dict__ = json.load(f, encoding="utf-8")
        except:
            self.Reset_Settings()

    def Reload(self, jsondata):
        self.__dict__ = json.loads(jsondata, encoding="utf-8")
        return

    def Save(self, settingsfile):
        try:
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="w+") as f:
                json.dump(self.__dict__, f, encoding="utf-8")
            with codecs.open(settingsfile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
                f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8')))
        except:
            Parent.Log(ScriptName, "Failed to save settings to file.")
        return

    def Reset_Settings(self):
        uiConfigDir = os.path.join(os.path.dirname(__file__), "..")
        uiCofigFile = os.path.join(uiConfigDir, "UI_Config.json")

        with codecs.open(uiCofigFile, encoding="utf-8-sig", mode="r") as f:
            dictionary = json.load(f, encoding="utf-8")

            for key in dictionary:
                if (not key in ["output_file"]) and "value" in dictionary[key].keys():
                    self.__dict__[key] = dictionary[key]["value"]

    def getCommands(self):
        return [
            self.faceitEloCommand
        ]