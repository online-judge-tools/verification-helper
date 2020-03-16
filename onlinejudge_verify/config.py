# Python Version: 3.x
import functools
import pathlib
from typing import *

import toml

config_path = pathlib.Path('.verify-helper/config.toml')


@functools.lru_cache(maxsize=None)
def get_config() -> Dict[str, Any]:
    if not config_path.exists():
        return {}
    return dict(toml.load(str(config_path)))
