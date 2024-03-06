from typing import Dict, Any

import yaml


def load_config(config_path: str = 'etc/config.yml') -> Dict[str, Any]:
    """
    Load and parse a YAML configuration file.

    :param config_path: The file path to the YAML configuration file. Defaults
        to 'etc/config.yml'.
    :return: A dictionary representation of the YAML configuration file's
        contents.
    """
    with open(config_path, 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    return cfg
