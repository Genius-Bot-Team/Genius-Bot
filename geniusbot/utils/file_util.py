import os


def touch_directory(directory_path: str):
    if not os.path.isdir(directory_path):
        os.makedirs(directory_path)
