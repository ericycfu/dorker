import yaml
import os

from dork.config.handlers import database_handler

class DorkerConfiguration(object):
    def __init__(self):
        self.config_hash = self.load_config()
        self.API_KEYS = self.config_hash['API_KEYS']
        self.CONFIGS = ['databases', 'misc']

        self.SOURCES = self.load_sources()

        self.HANDLERS = {
            'databases': database_handler.handle,
            'misc': database_handler.handle,
        }

    def load_sources(self):
        config_dir = os.path.join(os.getcwd(), 'lib/dork/config')
        configs = {}
        for config in self.CONFIGS:
            config_path = os.path.join(config_dir, "{}.yaml".format(config))
            stream = open(config_path, 'r')
            yaml_data = yaml.load(stream)
            configs[config] = yaml_data['Items']
        return configs

    def load_config(self):
        return yaml.load(open('config.yaml'))
