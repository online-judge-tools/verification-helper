import pathlib
from typing import *

import toml
from onlinejudge_verify.languages.base import Language
from onlinejudge_verify.languages.cplusplus import CPlusPlusLanguage
from onlinejudge_verify.languages.csharpscript import CSharpScriptLanguage
from onlinejudge_verify.languages.other import OtherLanguage

_dict: Dict[str, Language] = {}

_dict['.cpp'] = CPlusPlusLanguage()
_dict['.hpp'] = _dict['.cpp']
_dict['.csx'] = CSharpScriptLanguage()

config_path = pathlib.Path('.verify-helper/config.toml')
if config_path.exists():
    for ext, config in toml.load(str(config_path)).get('languages', {}).items():
        _dict['.' + ext] = OtherLanguage(config=config)


def get(path: pathlib.Path) -> Optional[Language]:
    return _dict.get(path.suffix)
