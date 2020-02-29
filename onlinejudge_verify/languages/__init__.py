import pathlib
from typing import *

import toml
from onlinejudge_verify.languages.base import Language
from onlinejudge_verify.languages.cplusplus import CPlusPlusLanguage
from onlinejudge_verify.languages.csharpscript import CSharpScriptLanguage
from onlinejudge_verify.languages.other import OtherLanguage

_dict: Dict[str, Language] = {}

_dict['.test.cpp'] = CPlusPlusLanguage()
_dict['.test.hpp'] = _dict['.test.cpp']
_dict['.test.csx'] = CSharpScriptLanguage()

config_path = pathlib.Path('.verify-helper/config.toml')
if config_path.exists():
    for ext, config in toml.load(str(config_path)).get('languages', {}).items():
        suffix = config.get('suffix', '.test.' + ext)
        _dict[suffix] = OtherLanguage(config=config)


def get(path: pathlib.Path) -> Optional[Language]:
    for suffix, language in _dict.items():
        if str(path.name).endswith(suffix):
            return language
    else:
        return None
