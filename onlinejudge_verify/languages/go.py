from typing import *

from onlinejudge_verify.config import get_config
from onlinejudge_verify.languages.user_defined import UserDefinedLanguage


# TODO: stop using UserDefinedLanguage
class GoLanguage(UserDefinedLanguage):
    config: Dict[str, Any]

    def __init__(self, *, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the configuration.

        Args:
            self: (todo): write your description
            config: (dict): write your description
            Optional: (todo): write your description
            Dict: (todo): write your description
            str: (todo): write your description
            Any: (float): write your description
        """
        if config is None:
            config = get_config().get('languages', {}).get('go', {})
        config.setdefault('compile', 'echo')
        config.setdefault('execute', 'go run {basedir}/{path}')
        super().__init__(extension='go', config=config)
