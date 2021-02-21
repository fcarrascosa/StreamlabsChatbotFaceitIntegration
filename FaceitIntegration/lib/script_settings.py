import codecs
import json
import os

NON_PROPERTY_KEYS = [
    'output_file'
]

CORE_REQUIRED_KEYS = [
    'faceit_api_key'
]


class FaceitIntegrationSettings(object):
    def __init__(self, settings_file=None):
        try:
            with codecs.open(settings_file, encoding='utf-8-sig', mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8')
        except:
            self.reset_settings()

    def reset_settings(self):
        """ Resets the settings to the default values set on UI_Config.json file
        :return: void
        """
        ui_config_dir = os.path.join(os.path.dirname(__file__), '..')
        ui_config_file = os.path.join(ui_config_dir, 'UI_Config.json')
        with codecs.open(ui_config_file, encoding='utf-8-sig', mode='r') as f:
            dictionary = json.load(f, encoding='utf-8')
            for key in dictionary:
                if key not in NON_PROPERTY_KEYS and 'value' in dictionary[key].keys():
                    self.__dict__[key] = dictionary[key]['value']

    def save(self, settings_file, script_name='', parent=None):
        try:
            with codecs.open(settings_file, encoding='utf-8-sig', mode='w+') as f:
                json.dump(self.__dict__, f, encoding='utf-8')
            with codecs.open(settings_file.replace('.json', '.js'), encoding='utf-8-sig', mode='w+') as f:
                f.write('const settings = {0};'.format(json.dumps(self.__dict__, encoding='utf-8')))
        except:
            parent.Log(script_name, "Failed to save settings file")

    def load_settings(self, json_data):
        self.__dict__ = json.loads(json_data, encoding="utf-8")

    def validate_core_fields(self):
        """

        :return: bool
        """
        return_value = True
        for key in CORE_REQUIRED_KEYS:
            return_value = return_value if return_value and self.__getattribute__(key) else False
        return return_value
