import os
import sys

from distutils.version import StrictVersion

sys.path.append(os.path.dirname(__file__))

from lib.Settings import Settings
from lib.utils.messaging import show_confirm_dialog, get_message, show_dialog
from lib.utils.requests import make_get_request

# ---------------------------
#   Script Information
# ---------------------------

ScriptName = "FaceitIntegration"
Website = "https://fcarrascosa.es"
Description = "A simple script to integrate Streamlabs Chatbot with FaceIT Api"
Creator = "Fernando Carrascosa"
Version = "1.2.1"

# ---------------------------
#   Global Variables
# ---------------------------
global SETTINGS
SETTINGS_DIRECTORY = os.path.join(os.path.dirname(__file__), "settings")
SETTINGS_FILE = os.path.join(SETTINGS_DIRECTORY, "settings.json")


# ---------------------------
#   Lifecycle functions
# ---------------------------

def Init():
    """ [Required] Initialize Data (Only called on load)
    :return: void
    """

    if not os.path.exists(SETTINGS_DIRECTORY):
        os.makedirs(SETTINGS_DIRECTORY)

    global SETTINGS
    SETTINGS = Settings(Parent, SETTINGS_FILE)
    validate_settings()

    if SETTINGS.notification_on_new_version:
        check_version()


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
    global SETTINGS

    SETTINGS.load(json_data)
    validate_settings()
    return


# ---------------------------
#   Settings Functions
# ---------------------------
def validate_settings():
    if not SETTINGS.validate():
        show_dialog(get_message('config', 'error_config_header'), get_message('config', 'error_config_body'))


def reset_settings():
    if show_confirm_dialog(get_message('settings', 'reset_settings_confirm_header'),
                           get_message('settings', 'reset_settings_confirm_body')):
        SETTINGS.reset(SETTINGS_FILE)
        show_dialog(get_message('settings', 'reset_settings_success_header'),
                    get_message('settings', 'reset_settings_success_body'))
        validate_settings()


# ---------------------------
#   Miscellaneous Functions
# ---------------------------

def check_version():
    releases_url = 'https://api.github.com/repos/fcarrascosa/StreamlabsChatbotFaceitIntegration/releases/latest'
    current_version = StrictVersion(Version)

    try:
        latest_version_tag = make_get_request(Parent, releases_url)['tag_name'].replace('v', '')
        latest_version = StrictVersion(latest_version_tag)

        if latest_version > current_version:
            new_version_body = get_message('versioning', 'new_version_body').replace('{VERSION_NAME}',
                                                                                     latest_version_tag)
            if show_confirm_dialog(get_message('versioning', 'new_version_header'), new_version_body):
                os.system("explorer https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/releases/")

    except:
        Parent.Log(
            get_message('versioning', 'log_version_error_title'),
            get_message('versioning', 'log_version_error_description')
        )


def open_donation():
    os.system("explorer https://ko-fi.com/fcarrascosa")
