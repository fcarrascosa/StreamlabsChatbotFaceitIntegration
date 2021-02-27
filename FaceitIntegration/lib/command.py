from faceit_api_client import FaceitApiClient


class Command(object):
    def __init__(self, parent, settings, name, script_name, data):
        self.parent = parent
        self.settings = settings
        self.name = name.replace('_command', '')
        self.script_name = script_name
        self.user = data.User
        self.user_name = data.UserName
        self.data = data
        return

    def get_settings_attribute(self, attribute=''):
        return self.settings.__getattribute__(self.name + '_' + attribute)

    def get_command_name(self):
        return self.get_settings_attribute('command')

    def get_permission(self):
        return self.get_settings_attribute('permission')

    def get_permission_specific(self):
        return self.get_settings_attribute('permission_specific')

    def get_cooldown(self):
        return self.get_settings_attribute('cooldown')

    def get_message(self):
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
            self.settings.faceit_elo_command: FaceitApiClient(self.settings.faceit_api_key, self.parent).get_player_elo
        }

        message = self.get_message()

        try:
            parse_options = function_per_command[self.get_command_name()](
                self.data.GetParam(1) if self.data.GetParam(1) else self.get_default_argument())
        except:
            parse_options = {}
            message = self.get_error_message()

        message = self.parse_command_message(message, parse_options)
        self.parent.SendStreamMessage(message)
        return
