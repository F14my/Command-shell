import os


def get_curr_dir():
    curr_dir = os.getcwd().replace("\\", "/")
    home_dir = os.path.expanduser("~")
    if curr_dir.startswith(home_dir):
        curr_dir = "~" + curr_dir[len(home_dir):]
    return curr_dir