from faceit_api_client import FaceitApiClient
import time
import datetime


class Command(object):
    def __init__(self, parent, settings, name, script_name, data, analyzer=None):
        self.parent = parent
        self.settings = settings
        self.name = name.replace('_command', '')
        self.script_name = script_name
        self.user = data.User if data else None
        self.user_name = data.UserName if data else None
        self.data = data
        self.analyzer = analyzer
        return

    def get_settings_attribute(self, attribute=''):
        return self.settings.__getattribute__(self.name + '_' + attribute) if self.name + '_' + attribute in self.settings.__dict__ else ''

    def get_command_name(self):
        return self.get_settings_attribute('command')

    def get_permission(self):
        return self.get_settings_attribute('permission')

    def get_permission_specific(self):
        return self.get_settings_attribute('permission_specific')

    def get_cooldown(self):
        return self.get_settings_attribute('cooldown')

    def get_message(self, ):
        return self.get_settings_attribute('message')

    def get_default_argument(self):
        return self.get_settings_attribute('default_argument')

    def get_error_message(self):
        return self.get_settings_attribute('error_message')

    def get_cooldown_message(self):
        return self.settings.__getattribute__('faceit_cooldown_message')

    def get_permission_message(self):
        return self.settings.__getattribute__('faceit_permission_message')

    def set_cooldown_for_command(self):
        self.parent.AddUserCooldown(self.script_name, self.name, self.user, self.get_cooldown())
        return

    def check_cooldown_for_command(self):
        return self.parent.IsOnUserCooldown(self.script_name, self.name, self.user)

    def check_permission_for_command(self):
        return self.parent.HasPermission(self.user, self.get_permission(), self.get_permission_specific())

    def parse_command_message(self, message_to_parse, parsing_keys={}):
        message = message_to_parse
        message = message.replace('$command', self.get_command_name())
        message = message.replace('$username', self.user_name)
        message = message.replace('$arg1',
                                  self.data.GetParam(1) if self.data.GetParam(1) else self.get_default_argument())
        message = message.replace('$cooldownTimer',
                                  str(self.parent.GetUserCooldownDuration(self.script_name, self.name, self.user)))
        for key, value in parsing_keys.items():
            message = message.replace("$" + key, str(value))
        return message

    def execute_command(self):
        if not self.check_permission_for_command():
            permission_message = self.get_permission_message()
            permission_message = self.parse_command_message(permission_message)
            self.parent.SendStreamMessage(permission_message)
            return
        if self.check_cooldown_for_command():
            cooldown_message = self.get_cooldown_message()
            cooldown_message = self.parse_command_message(cooldown_message)
            self.parent.SendStreamMessage(cooldown_message)
            return
        else:
            self.set_cooldown_for_command()

        function_per_command = {
            self.settings.faceit_elo_command: FaceitApiClient(self.settings.faceit_api_key, self.parent).get_player_elo,
            self.settings.faceit_session_start_command: self.init_session,
            self.settings.faceit_session_command: self.get_session,
        }

        message = self.get_message()

        try:
            parse_options = function_per_command[self.get_command_name()](
                self.data.GetParam(1) if self.data.GetParam(1) else self.get_default_argument())
        except:
            parse_options = {}
            message = self.get_error_message()

        message = self.parse_command_message(message, parse_options if parse_options else {})
        self.parent.SendStreamMessage(message)
        return

    def get_session(self, *args):
        match_history = FaceitApiClient(self.settings.faceit_api_key, self.parent).get_match_history(
            self.settings.faceit_session_default_argument, self.analyzer.session_init)
        current_elo = FaceitApiClient(self.settings.faceit_api_key, self.parent).get_player_elo(
            self.settings.faceit_session_default_argument)
        self.analyzer.set_matches(match_history if len(match_history) else [])
        return {
            "total_matches": self.analyzer.count_total_matches(),
            "won_matches": self.analyzer.count_won_matches(),
            "lost_matches": self.analyzer.count_lost_matches(),
            "elo_balance": self.analyzer.get_session_elo(current_elo["elo"])
        }

    def init_session(self, *args):
        now = int(time.mktime(datetime.datetime.now().timetuple()))
        api_client = FaceitApiClient(self.settings.faceit_api_key, self.parent)
        initial_elo = api_client.get_player_elo(self.settings.faceit_session_default_argument)["elo"]
        initial_matches = api_client.get_match_history(self.settings.faceit_session_default_argument, now)
        self.analyzer.start_session(initial_elo, initial_matches)
        self.analyzer.matches = []

        return