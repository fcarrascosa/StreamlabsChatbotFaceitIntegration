import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
from file_system import create_directory

# ---------------------------
#   Script Information
# ---------------------------

ScriptName = "FaceitIntegration"
Website = "https://fcarrascosa.es"
Description = "A simple script to integrate Streamlabs Chatbot with FaceIT Api"
Creator = "Fernando Carrascosa"
Version = "0.3.1"

# ---------------------------
#   Global Variables
# ---------------------------
settings_directory = os.path.join(os.path.dirname(__file__), 'settings')
settings_file = os.path.join(settings_directory, 'settings.json')


# ---------------------------
#   Lifecycle functions
# ---------------------------

def Init():
    """ [Required] Initialize Data (Only called on load)
    :return: void
    """

    create_directory(settings_directory)
    return


def Execute(data):
    """ [Required] Execute Data / Process messages
    :param data: the Data object provided by SLCB
    :return: void
    """

    return


def Tick():
    """ [Required] Tick method (Gets called during every iteration even when there is no incoming data)
    :return: void
    """

    return
