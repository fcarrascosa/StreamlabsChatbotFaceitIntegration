class Command(object):
    def __init__(self, parent, settings, name, script_name, user, user_name, data):
        self.parent = parent
        self.settings = settings
        self.name = name.replace('_command', '')
        self.script_name = script_name
        self.user = user
        self.user_name = user_name
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

    def parse_command_message(self, message_to_parse):
        message = message_to_parse
        message = message.replace('$command', self.get_command_name())
        message = message.replace('$username', self.user_name)
        message = message.replace('$arg1',
                                  self.data.GetParam(1) if self.data.GetParam(1) else self.get_default_argument())
        message = message.replace('$cooldownTimer',
                                  str(self.parent.GetUserCooldownDuration(self.script_name, self.name, self.user)))
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

        message = self.get_message()
        message = self.parse_command_message(message)
        self.parent.SendStreamMessage(message)
        return
