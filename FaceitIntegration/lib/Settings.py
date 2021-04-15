import codecs
import json
import os
from copy import deepcopy

from utils.dictionaries import clean

CORE_REQUIRED_KEYS = [
    'faceit_api_key',
    'faceit_username'
]

NON_PROPERTY_KEYS = [
    'output_file',
    'button_set_defaults',
    'button_donate'
]

KEYS_TO_EXCLUDE = [
    'parent'
]


class Settings:
    def __init__(self, parent, settings_file=None):
        if settings_file and os.path.isfile(settings_file):
            with codecs.open(settings_file, encoding='utf-8-sig', mode='r') as f:
                self.__dict__.update(**json.load(f, encoding='utf-8-sig'))
        else:
            self.reset(settings_file)

        self.parent = parent

    def reset(self, settings_file):
        ui_config_dir = os.path.join(os.path.dirname(__file__), '..')
        ui_config_file = os.path.join(ui_config_dir, 'UI_Config.json')

        with codecs.open(ui_config_file, encoding="utf-8-sig", mode='r') as f:
            settings_object = json.load(f, encoding='utf-8-sig')
            for key in settings_object:
                if key not in NON_PROPERTY_KEYS and 'value' in settings_object[key].keys():
                    self.__dict__[key] = settings_object[key]['value']
        self.save(settings_file)

    def save(self, settings_file):
        dict_copy = deepcopy(self.__dict__)
        dict_copy = clean(dict_copy, KEYS_TO_EXCLUDE)

        try:
            with codecs.open(settings_file, encoding='utf-8-sig', mode='w+') as f:
                json.dump(dict_copy, f, encoding='utf-8', ensure_ascii=False)
            with codecs.open(settings_file.replace('.json', '.js'), encoding='utf-8-sig', mode='w+') as f:
                f.write(
                    'var settings = {0};'.format(json.dumps(dict_copy, f, encoding='utf-8', ensure_ascii=False)))
        except ValueError:
            self.parent.Log(settings_file, 'Failed to save settings to file.')

    def load(self, data):
        self.__dict__.update(**json.loads(data, encoding='utf-8-sig'))

    def validate(self):
        return_value = True
        for key in CORE_REQUIRED_KEYS:
            return_value = return_value if return_value and self.__dict__[key] else False

        return return_value
