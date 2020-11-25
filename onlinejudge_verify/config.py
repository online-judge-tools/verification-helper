# Python Version: 3.x
import pathlib
from logging import getLogger
from typing import *

import toml

logger = getLogger(__name__)

default_config_path = pathlib.Path('.verify-helper/config.toml')

_loaded_config: Optional[Dict[str, Any]] = None


def set_config_path(config_path: pathlib.Path) -> None:
    global _loaded_config  # pylint: disable=invalid-name
    assert _loaded_config is None
    if not config_path.exists():
        _loaded_config = {}
        logger.info('no config file')
    else:
        _loaded_config = dict(toml.load(str(config_path)))
        logger.info('config file loaded: %s: %s', str(config_path), _loaded_config)


def get_config() -> Dict[str, Any]:
    if _loaded_config is None:
        set_config_path(default_config_path)
    assert _loaded_config is not None
    return _loaded_config
