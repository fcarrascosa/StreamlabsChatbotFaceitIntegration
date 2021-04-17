from errors.CooldownError import CooldownError
from errors.ExecutionError import ExecutionError
from errors.PermissionError import PermissionError


class Command:
    def __init__(self,
                 parent,
                 script_name,
                 command_key,
                 permission,
                 permission_specific,
                 global_cooldown,
                 user_cooldown,
                 user,
                 user_name,
                 ):
        self.parent = parent
        self.script_name = script_name
        self.command_key = command_key
        self.permission = permission
        self.permission_specific = permission_specific
        self.global_cooldown = global_cooldown
        self.user = user
        self.user_name = user_name
        self.user_cooldown = user_cooldown

    def user_has_permission(self):
        return self.parent.HasPermission(self.user, self.permission, self.permission_specific)

    def is_on_cooldown(self):
        return self.is_on_global_cooldown() or self.is_on_user_cooldown()

    def is_on_user_cooldown(self):
        return self.parent.IsOnUserCooldown(self.script_name, self.command_key, self.user)

    def is_on_global_cooldown(self):
        return self.parent.IsOnCooldown(self.script_name, self.command_key)

    def get_cooldown_duration(self):
        global_cooldown = self.get_global_cooldown()
        user_cooldown = self.get_user_cooldown()

        return global_cooldown if global_cooldown > user_cooldown else user_cooldown

    def get_global_cooldown(self):
        return self.parent.GetCooldownDuration(self.script_name, self.command_key)

    def get_user_cooldown(self):
        return self.parent.GetUserCooldownDuration(self.script_name, self.command_key, self.user)

    def set_cooldown(self):
        self.set_global_cooldown()
        self.set_user_cooldown()

    def set_global_cooldown(self):
        self.parent.AddCooldown(self.script_name, self.command_key, int(self.global_cooldown))

    def set_user_cooldown(self):
        self.parent.AddUserCooldown(self.script_name, self.command_key, self.user, int(self.user_cooldown))

    def execute(self, fn, arguments):
        if not self.user_has_permission():
            raise PermissionError()
        if self.is_on_cooldown():
            raise CooldownError()

        try:
            return fn(self.parent, arguments)
        except:
            raise ExecutionError()
