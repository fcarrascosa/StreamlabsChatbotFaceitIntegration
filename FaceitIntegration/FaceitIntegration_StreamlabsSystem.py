# ---------------------------
#   Import Libraries
# ---------------------------
import os
import sys
import json
import clr
import winsound
import ctypes

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))  # point at lib folder for classes / references
from FaceitIntegrationSettings import FaceitIntegrationSettings
from FaceitApiClient import FaceitApiClient

MessageBox = ctypes.windll.user32.MessageBoxW
MB_YES = 6

clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#   Import your Settings class

# ---------------------------
#   [Required] Script Information
# ---------------------------
ScriptName = "Faceit Integration"
Website = "https://fcarrascosa.es"
Description = "A simple script to integrate with faceit"
Creator = "Fernando Carrascosa"
Version = "1.0.0"

# ---------------------------
#   Define Global Variables
# ---------------------------
settingsDir = os.path.join(os.path.dirname(__file__), "Settings")
settingsFile = os.path.join(settingsDir, "settings.json")

global Settings
Settings = FaceitIntegrationSettings(settingsFile)


# ---------------------------
#   [Required] Initialize Data (Only called on load)
# ---------------------------
def Init():
    #   Create Settings Directory
    if not os.path.exists(settingsDir):
        os.makedirs(settingsDir)
    Settings.Save(settingsFile)

    checkApiKey(Settings)
    return


# ---------------------------
#   [Required] Execute Data / Process messages
# ---------------------------
def Execute(data):
    if data.IsChatMessage() and data.GetParam(0).lower() in Settings.getCommands():
        functionPerCommand = {
            Settings.faceitEloCommand: playerElo
        }

        functionPerCommand[data.GetParam(0).lower()](data)

    return


# ---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
# ---------------------------
def Tick():
    return


# ---------------------------
#   [Optional] Parse method (Allows you to create your own custom $parameters) 
# ---------------------------
def Parse(parseString, userid, username, targetid, targetname, message):
    return parseString


# ---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
# ---------------------------
def ReloadSettings(jsonData):
    # Execute json reloading here
    Settings.__dict__ = json.loads(jsonData)
    Settings.Save(settingsFile)
    checkApiKey(Settings)
    return


# ---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
# ---------------------------
def Unload():
    return


# ---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
# ---------------------------
def ScriptToggled(state):
    return


# ------------------------------------------------------------
#   Settings functions
# ------------------------------------------------------------

# ---------------------------
#   Sets default options
# ---------------------------
def setDefaults():
    winsound.MessageBeep()
    returnValue = MessageBox(0, u"You are about to reset the settings.\n"
                                u"Are you sure you want to continue?"
                             , u"Reset settings file", 4)

    if returnValue == MB_YES:
        if os.path.exists(settingsFile):
            os.remove(settingsFile)
            os.remove(os.path.join(settingsDir, "settings.js"))
        Settings.Reset_Settings()
        MessageBox(0, u"Settings successfully restored to default values"
                   , u"Reset complete!", 0)
    checkApiKey(Settings)
    return


# ---------------------------
#   Checks for faceit api key
# ---------------------------
def checkApiKey(settings):
    if not settings.faceitApiKey:
        MessageBox(0, u"Remember to set your Faceit API key in the settings"
                   , u"API KEY MISSING!", 0)
    return


def checkFaceitEloDefaultUser(settings):
    if not settings.faceitEloDefaultUser:
        Parent.SendStreamMessage("There is no default player configured for this command.")
    return settings.faceitEloDefaultUser


# ------------------------------------------------------------
#   Validator functions
# ------------------------------------------------------------

# ---------------------------
#   Checking cooldown for command
# ---------------------------

def checkCooldown(data):
    cooldownMessages = [

    ]

# ------------------------------------------------------------
#   Action functions
# ------------------------------------------------------------

# ---------------------------
#   Gets the faceit elo for a player
# ---------------------------
def playerElo(data):
    if not checkFaceitEloDefaultUser(Settings):
        return

    client = FaceitApiClient(Settings.faceitApiKey, Parent)
    player = data.GetParam(1) if data.GetParam(1) else Settings.faceitEloDefaultUser
    try:
        elo = client.getPlayerElo(player)
        message = Settings.faceitEloMessage
        message = message.replace("$value", elo)
    except:
        message = Settings.faceitEloErrorMessage

    message = message.replace("$username", data.UserName).replace("$arg1", player)
    Parent.SendStreamMessage(message)
