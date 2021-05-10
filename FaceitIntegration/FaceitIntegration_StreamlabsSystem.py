import os
import sys
from distutils.version import StrictVersion
import time
from datetime import datetime

sys.path.append(os.path.dirname(__file__))

from lib.actions.session import init_session, get_session_analysis, get_session_analysis_deprecated
from lib.Command import Command
from lib.errors.CooldownError import CooldownError
from lib.errors.ExecutionError import ExecutionError
from lib.errors.PermissionError import PermissionError
from lib.Settings import Settings
from lib.utils.commands import FUNCTION_PER_COMMAND
from lib.utils.execute import should_check_command
from lib.utils.messaging import show_confirm_dialog, get_message, show_dialog, build_message
from lib.utils.requests import make_get_request

# ---------------------------
#   Script Information
# ---------------------------

ScriptName = "FaceitIntegration"
Website = "https://fcarrascosa.es"
Description = "A simple script to integrate Streamlabs Chatbot with FaceIT Api"
Creator = "Fernando Carrascosa"
Version = "2.0.0"

# ---------------------------
#   Global Variables
# ---------------------------
global SETTINGS
SETTINGS_DIRECTORY = os.path.join(os.path.dirname(__file__), "settings")
SETTINGS_FILE = os.path.join(SETTINGS_DIRECTORY, "settings.json")
global LAST_TIME_CHECKED
LAST_TIME_CHECKED = int(time.mktime(datetime.now().timetuple()))


# ---------------------------
#   Lifecycle functions
# ---------------------------

def Init():
    """ [Required] Initialize Data (Only called on load)
    :return: None
    """

    if not os.path.exists(SETTINGS_DIRECTORY):
        os.makedirs(SETTINGS_DIRECTORY)

    global SETTINGS
    SETTINGS = Settings(Parent, SETTINGS_FILE)
    validate_settings()

    if SETTINGS.faceit_start_session_start_on_load:
        init_analyzer_session()

    if SETTINGS.notification_on_new_version:
        check_version()


def Execute(data):
    """ [Required] Execute Data / Process messages
    :param data: the Data object provided by SLCB
    :return: None
    """
    if should_check_command(data):
        global SETTINGS
        commands_triggers = SETTINGS.get_commands()
        command_candidate = data.GetParam(0)

        if command_candidate in commands_triggers.values():
            command_key = commands_triggers.keys()[commands_triggers.values().index(command_candidate)]

            commands_global_cooldown = SETTINGS.get_commands_global_cooldown()
            command_global_cooldown = commands_global_cooldown[
                command_key] if command_key in commands_global_cooldown.keys() else 0
            commands_user_cooldown = SETTINGS.get_commands_user_cooldown()
            command_user_cooldown = commands_user_cooldown[
                command_key] if command_key in commands_user_cooldown.keys() else 0

            command = Command(
                parent=Parent,
                script_name=ScriptName,
                command_key=command_key,
                permission=SETTINGS.get_commands_permission()[command_key],
                permission_specific=SETTINGS.get_commands_permission_specific()[command_key],
                global_cooldown=command_global_cooldown,
                user_cooldown=command_user_cooldown,
                user=data.User,
                user_name=data.UserName,
            )

            params = {
                'command': command_candidate,
                'username': data.UserName,
                'player': data.GetParam(1) or SETTINGS.faceit_username
            }

            try:
                arguments = {
                    'default_player': SETTINGS.faceit_username,
                    'api_key': SETTINGS.faceit_api_key,
                    'overlays_enabled': SETTINGS.overlays_enabled,
                    'argument': data.GetParam(1),
                    'include_all_matches': SETTINGS.faceit_session_include_all_matches,
                }
                command_execution = command.execute(FUNCTION_PER_COMMAND[command_key], arguments)

                if command_execution:
                    params.update(command_execution)

                command.set_cooldown()
                message = SETTINGS.get_commands_success_message()[command_key]
            except CooldownError:
                message = SETTINGS.faceit_cooldown_message.replace('$username', data.UserName)
                params.update({'cooldownTimer': str(command.get_cooldown_duration())})
            except PermissionError:
                message = SETTINGS.faceit_permission_message
            except ExecutionError:
                message = SETTINGS.get_commands_error_message()[command_key]
            finally:
                if 'message' in locals():
                    Parent.SendStreamMessage(build_message(message, params))


def Tick():
    """ [Required] Tick method (Gets called during every iteration even when there is no incoming data)

    :return: None
    """
    if SETTINGS.overlays_enabled:
        current_time = int(time.mktime(datetime.now().timetuple()))
        global LAST_TIME_CHECKED
        if (current_time != LAST_TIME_CHECKED) and (current_time % 5 == 0):
            LAST_TIME_CHECKED = current_time
            get_analyzer_session(Parent, {
                'default_player': SETTINGS.faceit_username,
                'api_key': SETTINGS.faceit_api_key,
                'overlays_enabled': SETTINGS.overlays_enabled,
                'include_all_matches': SETTINGS.faceit_session_include_all_matches,
            })


def ReloadSettings(json_data):
    """[Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)

    :param json_data: the settings object
    :return: None
    """
    global SETTINGS

    SETTINGS.load(json_data)
    validate_settings()


def Unload():
    """ [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)

    :return: None
    """

def ScriptToggled(state):
    """ [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
    :param state:
    :return: None
    """


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


def open_docs():
    os.system("explorer https://github.com/fcarrascosa/StreamlabsChatbotFaceitIntegration/wiki")


# ---------------------------
#   Session Functions
# ---------------------------

def init_analyzer_session():
    arguments = {
        'default_player': SETTINGS.faceit_username,
        'api_key': SETTINGS.faceit_api_key,
        'overlays_enabled': SETTINGS.overlays_enabled,
        'include_all_matches': SETTINGS.faceit_session_include_all_matches
    }
    init_session(Parent, arguments)

    if SETTINGS.overlays_enabled:
        get_analyzer_session(Parent, arguments)


def get_analyzer_session(parent, options):
    # TODO: Replace this with get_session_analysis when FACEIT API gets FIXED
    get_session_analysis_deprecated(parent, options)
