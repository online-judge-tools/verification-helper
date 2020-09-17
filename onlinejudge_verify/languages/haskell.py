from typing import *

from onlinejudge_verify.config import get_config
from onlinejudge_verify.languages.user_defined import UserDefinedLanguage


# TODO: stop using UserDefinedLanguage
class HaskellLanguage(UserDefinedLanguage):
    config: Dict[str, Any]

    def __init__(self, *, config: Optional[Dict[str, Any]] = None):
        if config is None:
            config = get_config().get('languages', {}).get('haskell', {})
        config.setdefault('compile', 'echo')
        config.setdefault('execute', 'runghc {basedir}/{path}')
        super().__init__(extension='hs', config=config)
