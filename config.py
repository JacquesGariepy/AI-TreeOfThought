import json

def load_config(file_path='config.json'):
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
    return config
