# ---------------------------
#   Script Information
# ---------------------------

ScriptName = "FaceitIntegration"
Website = "https://fcarrascosa.es"
Description = "A simple script to integrate Streamlabs Chatbot with FaceIT Api"
Creator = "Fernando Carrascosa"
Version = "1.2.1"

# ---------------------------
#   Global Variables
# ---------------------------



# ---------------------------
#   Lifecycle functions
# ---------------------------

def Init():
    """ [Required] Initialize Data (Only called on load)
    :return: void
    """


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


def ReloadSettings(json_data):
    """[Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)

    :param json_data: the settings object
    :return: void
    """
    return
