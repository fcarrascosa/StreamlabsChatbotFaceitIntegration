import os


def create_directory(directory):
    """ Creates a directory if it does not exist

    :param directory: String
    :return: void
    """
    if not check_directory(directory):
        os.makedirs(directory)
    return


def check_directory(directory):
    """ Checks if a directory exists

    :param directory: String
    :return: bool
    """
    return os.path.exists(directory)
