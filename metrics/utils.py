import os


def remove_file_if_exists(path):
    if os.path.isfile(path):
        os.remove(path)
