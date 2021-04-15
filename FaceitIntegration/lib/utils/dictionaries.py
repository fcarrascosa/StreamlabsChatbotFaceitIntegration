from copy import deepcopy


def clean(dict_to_clear = {}, removable_keys=[]):
    keys_to_remove = ['__dict__'] + removable_keys

    dict_copy = deepcopy(dict_to_clear)
    for key in keys_to_remove:
        if key in dict_copy:
            dict_copy.pop(key)
    return dict_copy
