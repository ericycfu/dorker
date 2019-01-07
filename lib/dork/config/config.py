import yaml
import os

from dork.config.handlers import database_handler

CONFIGS = ['databases', 'misc']
HANDLERS = {
    'databases': database_handler.handle,
    'misc': database_handler.handle,
}

API_KEYS = []

def load_configs():
    config_dir = os.path.join(os.getcwd(), 'lib/dork/config')
    configs = {}
    for config in CONFIGS:
        config_path = os.path.join(config_dir, "{}.yaml".format(config))
        stream = open(config_path, 'r')
        yaml_data = yaml.load(stream)
        configs[config] = yaml_data['Items']
    return configs

def get_configs():
    return CONFIGS

def get_handlers():
    return HANDLERS

def get_api_keys():
    return API_KEYS
