import json
import os
import sys

def get_config_path():
    if getattr(sys, "frozen", False):
        return os.path.join(os.path.dirname(sys.executable), "config.json")

    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")


def load_config():
    with open(get_config_path(), "r") as file:
        return json.load(file)


config = load_config()
API_KEY = config["weather_api_key"]