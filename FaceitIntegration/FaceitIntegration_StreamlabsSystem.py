import codecs
import os
import sys
import json

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
sys.path.append(os.path.join(os.path.dirname(__file__), "assets"))
import messaging
from file_system import create_directory
from script_settings import FaceitIntegrationSettings
from command import Command

# ---------------------------
#   Script Information
# ---------------------------

ScriptName = "FaceitIntegration"
Website = "https://fcarrascosa.es"
Description = "A simple script to integrate Streamlabs Chatbot with FaceIT Api"
Creator = "Fernando Carrascosa"
Version = "1.1.1"

# ---------------------------
#   Global Variables
# ---------------------------
SETTINGS_DIRECTORY = os.path.join(os.path.dirname(__file__), "settings")
SETTINGS_FILE = os.path.join(SETTINGS_DIRECTORY, "settings.json")
SETTINGS = FaceitIntegrationSettings(SETTINGS_FILE)
ASSETS_DIRECTORY = os.path.join(os.path.dirname(__file__), "assets")
MESSAGES_DIRECTORY = os.path.join(ASSETS_DIRECTORY, "messages")
MESSAGE_BOX_YES = 6


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
    if SETTINGS.notification_on_new_version:
        check_new_version()
    return


def Execute(data):
    """ [Required] Execute Data / Process messages
    :param data: the Data object provided by SLCB
    :return: void
    """

    if data.IsChatMessage():
        possible_command = data.GetParam(0)
        commands = SETTINGS.get_commands()

        if possible_command in commands.values():
            command_key = commands.keys()[commands.values().index(possible_command)]
            command = Command(Parent, SETTINGS, command_key, ScriptName, data)
            command.execute_command()

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
        messaging.show_dialog(get_message("config", "error_config_header"), get_message("config", "error_config_body"))
    return


# ---------------------------
#   Messaging Functions
# ---------------------------
def get_message(message_type="", key=""):
    message_file = os.path.join(MESSAGES_DIRECTORY, message_type + ".json")
    with codecs.open(message_file, encoding="utf-8-sig", mode="r") as f:
        obj = json.load(f, encoding="utf-8")
    return obj[key]


def check_new_version():
    current_version = Version.split(".")
    github_request = Parent.GetRequest(
        "https://api.github.com/repos/fcarrascosa/StreamlabsChatbotFaceitIntegration/releases/latest", {})
    github_response_object = json.loads(github_request)
    parsed_github_response_object = json.loads(github_response_object["response"])
    new_version_string = parsed_github_response_object["tag_name"]
    latest_version = new_version_string.replace("v", "").split(".")

    major_bump = current_version[0] < latest_version[0]
    minor_bump = not major_bump and current_version[1] < latest_version[1]
    patch_bump = not minor_bump and current_version[2] < latest_version[2]

    if major_bump or minor_bump or patch_bump:

        download_new_version = messaging.show_confirm_dialog(
            get_message("config", "new_version_header"),
            get_message("config", "new_version_body").replace("{VERSION_NAME}", new_version_string))

        if download_new_version == MESSAGE_BOX_YES:
            os.system("explorer https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/releases/")
    return
