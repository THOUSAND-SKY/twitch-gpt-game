import os

from dotenv import load_dotenv


def app_file_path(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "..", filename)


def read_app_file(filename):
    with open(app_file_path(filename)) as f:
        return f.read()


def read_dotenv():
    load_dotenv(app_file_path("../.env.local"))
    load_dotenv(app_file_path("../.env"))
