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

_dict['.cpp'] = CPlusPlusLanguage()
_dict['.hpp'] = _dict['.cpp']
_dict['.csx'] = CSharpScriptLanguage()

config_path = pathlib.Path('.verify-helper/config.toml')
if config_path.exists():
    for ext, config in toml.load(str(config_path)).get('languages', {}).items():
        logger.warn("%s: languages.%s: Adding new languages using `config.toml` is supported but not recommended. Please consider making pull requests for your languages, see https://github.com/kmyk/online-judge-verify-helper/issues/116", str(config_path), ext)
        _dict['.' + ext] = OtherLanguage(config=config)


def get(path: pathlib.Path) -> Optional[Language]:
    return _dict.get(path.suffix)
