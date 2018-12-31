import yaml
import os

CONFIGS = ['databases',]
def load_configs():
    config_dir = os.path.join(os.getcwd(), 'dork/config')
    configs = {}
    for config in CONFIGS:
        config_path = os.path.join(config_dir, "{}.yaml".format(config))
        stream = open(config_path, 'r')
        yaml_data = yaml.load(stream)
        configs[config] = yaml_data['Items']
    return configs

def get_configs():
    return CONFIGS
