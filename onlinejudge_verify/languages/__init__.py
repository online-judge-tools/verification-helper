import toml
import pathlib
from typing import *

from onlinejudge_verify.languages.base import Language
from onlinejudge_verify.languages.CPlusPlus import CPlusPlusLanguage
from onlinejudge_verify.languages.Other import OtherLanguage

_dict: Dict[str, Language] = {}

_dict['.cpp'] = CPlusPlusLanguage()
_dict['.hpp'] = _dict['.cpp']

config_path = pathlib.Path('.verify-helper/config.toml')
if config_path.exists():
    for ext, config in toml.load(str(config_path)).get('languages', {}).items():
        _dict['.' + ext] = OtherLanguage(config=config)


def get(path: pathlib.Path) -> Optional[Language]:
    return _dict.get(path.suffix)
