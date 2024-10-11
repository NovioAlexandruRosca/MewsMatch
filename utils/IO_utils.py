import json
import pandas as pd


def load_from_excel(file_path):
    return pd.read_excel(file_path)


def load_from_json(config_path):
    with open(config_path, "r") as file:
        data = json.load(file)
    return data
