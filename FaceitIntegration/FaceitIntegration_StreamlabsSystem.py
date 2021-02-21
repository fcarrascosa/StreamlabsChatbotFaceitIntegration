import codecs
import os
import sys
import json
from collections import namedtuple

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
sys.path.append(os.path.join(os.path.dirname(__file__), "assets"))
import messaging
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
ASSETS_DIRECTORY = os.path.join(os.path.dirname(__file__), 'assets')
MESSAGES_DIRECTORY = os.path.join(ASSETS_DIRECTORY, 'messages')


# ---------------------------
#   Lifecycle functions
# ---------------------------

def Init():
    """ [Required] Initialize Data (Only called on load)
    :return: void
    """

    create_directory(SETTINGS_DIRECTORY)
    SETTINGS.save(SETTINGS_FILE, ScriptName, Parent)
    validate_settings()
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
    SETTINGS.save(SETTINGS_FILE, ScriptName, Parent)
    validate_settings()
    return


# ---------------------------
#   Validation Functions
# ---------------------------
def validate_settings():
    if not SETTINGS.validate_core_fields():
        messaging.show_dialog(get_message('config', 'error_config_header'), get_message('config', 'error_config_body'))
    return


# ---------------------------
#   Messaging Functions
# ---------------------------
def get_message(message_type='', key=''):
    message_file = os.path.join(MESSAGES_DIRECTORY, message_type + '.json')
    with codecs.open(message_file, encoding='utf-8-sig', mode='r') as f:
        obj = json.load(f, encoding='utf-8')
    return obj[key]
