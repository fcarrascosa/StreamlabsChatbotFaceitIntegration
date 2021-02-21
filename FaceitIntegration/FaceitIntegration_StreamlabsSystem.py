import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
from file_system import create_directory
from script_settings import FaceitIntegrationSettings

# ---------------------------
#   Script Information
# ---------------------------

ScriptName = "FaceitIntegration"
Website = "https://fcarrascosa.es"
Description = "A simple script to integrate Streamlabs Chatbot with FaceIT Api"
Creator = "Fernando Carrascosa"
Version = "0.3.1"

# ---------------------------
#   Global Variables
# ---------------------------
SETTINGS_DIRECTORY = os.path.join(os.path.dirname(__file__), 'settings')
SETTINGS_FILE = os.path.join(SETTINGS_DIRECTORY, 'settings.json')
SETTINGS = FaceitIntegrationSettings()


# ---------------------------
#   Lifecycle functions
# ---------------------------

def Init():
    """ [Required] Initialize Data (Only called on load)
    :return: void
    """

    create_directory(SETTINGS_DIRECTORY)
    SETTINGS.save(SETTINGS_FILE, ScriptName, Parent)
    return


def Execute(data):
    """ [Required] Execute Data / Process messages
    :param data: the Data object provided by SLCB
    :return: void
    """

    return


def Tick():
    """ [Required] Tick method (Gets called during every iteration even when there is no incoming data)
    :return: void
    """

    return


def ReloadSettings(json_data):
    """[Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)

    :param json_data: the settings object
    :return: void
    """

    SETTINGS.load_settings(json_data)
    Parent.Log("SYSTEM", "RELOAD SETTINGS")
    SETTINGS.save(SETTINGS_FILE, ScriptName, Parent)
    return