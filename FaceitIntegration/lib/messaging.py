import winsound
import ctypes

MESSAGE_BOX = ctypes.windll.user32.MessageBoxW
MESSAGE_BOX_YES = 6


def show_confirm_dialog(header_message='', body_message=''):
    winsound.MessageBeep()
    return_value = MESSAGE_BOX(0, body_message, header_message, 4)


def show_dialog(header_message='', body_message=''):
    winsound.MessageBeep()
    return_value = MESSAGE_BOX(0, body_message, header_message, 0)
