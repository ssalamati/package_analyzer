from typing import Dict, Any

import yaml


def load_config(config_path: str = 'etc/config.yml') -> Dict[str, Any]:
    with open(config_path, 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    return cfg
