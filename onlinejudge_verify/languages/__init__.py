import pathlib
from logging import getLogger
from typing import *

import toml
from onlinejudge_verify.languages.base import Language
from onlinejudge_verify.languages.cplusplus import CPlusPlusLanguage
from onlinejudge_verify.languages.csharpscript import CSharpScriptLanguage
from onlinejudge_verify.languages.other import OtherLanguage

logger = getLogger(__name__)

_dict: Dict[str, Language] = {}

_dict['.test.cpp'] = CPlusPlusLanguage()
_dict['.test.hpp'] = _dict['.test.cpp']
_dict['.test.csx'] = CSharpScriptLanguage()

config_path = pathlib.Path('.verify-helper/config.toml')
if config_path.exists():
    for ext, config in toml.load(str(config_path)).get('languages', {}).items():
        logger.warn("%s: languages.%s: Adding new languages using `config.toml` is supported but not recommended. Please consider making pull requests for your languages, see https://github.com/kmyk/online-judge-verify-helper/issues/116", str(config_path), ext)
        suffix = config.get('suffix', '.test.' + ext)
        _dict[suffix] = OtherLanguage(config=config)


def get(path: pathlib.Path) -> Optional[Language]:
    for suffix, language in _dict.items():
        if str(path.name).endswith(suffix):
            return language
    else:
        return None
