import codecs
import json
import os
import winsound
import ctypes

MESSAGE_BOX = ctypes.windll.user32.MessageBoxW

ASSETS_DIRECTORY = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
MESSAGES_DIRECTORY = os.path.join(ASSETS_DIRECTORY, 'messages')

MESSAGE_BOX_TYPE = {
    'OK': 0x00000000L,
    'OK_CANCEL': 0x00000001L,
    'ABORT_RETRY_IGNORE': 0x00000002L,
    'YES_NO_CANCEL': 0x00000003L,
    'YES_NO': 0x00000004L,
    'RETRY_CANCEL': 0x00000005L,
    'CANCEL_RETRY_CONTINUE': 0x00000006L,
    'HELP': 0x00004000L
}

MESSAGE_BOX_RESPONSE = {
    'OK': 1,
    'CANCEL': 2,
    'ABORT': 3,
    'RETRY': 4,
    'IGNORE': 5,
    'YES': 6,
    'NO': 7,
    'TRYAGAIN': 10,
    'CONTINUE': 11,
}


def show_confirm_dialog(header_message='', body_message=''):
    winsound.MessageBeep()
    box_result = MESSAGE_BOX(0, body_message, header_message, MESSAGE_BOX_TYPE['YES_NO'])
    return box_result == MESSAGE_BOX_RESPONSE['YES']


def show_dialog(header_message='', body_message=''):
    winsound.MessageBeep()
    MESSAGE_BOX(0, body_message, header_message, MESSAGE_BOX_TYPE['OK'])
    return True


def get_message(message_type='', key=''):
    message_file = os.path.join(MESSAGES_DIRECTORY, message_type + '.json')
    with codecs.open(message_file, encoding='utf-8-sig', mode='r') as f:
        obj = json.load(f, encoding='utf-8')
    return obj[key]


def build_message(message='', values=None):
    if values is not None and isinstance(values, dict):
        result = message

        for key, value in values.items():
            result = result.replace('$' + key, str(value))
        return result
    else:
        return message
