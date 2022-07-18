import logging
import os
from logging import config
from typing import Union

from lazier.properties import properties
from lazier.utils import load_properties


class LogConfigurer:
    @classmethod
    def configure(cls, conf: Union[str, dict], level: Union[int, str] = logging.DEBUG, filepath: str = './logs'):
        try:
            conf = properties(
                load_properties(conf),
                {"logging": {"level": level}} if level else {},
                {"logging": {"filename": os.path.basename(filepath)}} if filepath else {},
                {"logging": {"filepath": os.path.dirname(filepath)}} if filepath else {},
            )
            logging.config.dictConfig(conf)
        except Exception as e:
            logging.getLogger().exception(e)


# for test
if __name__ == "__main__":
    print(os.path.basename('/abc.ddd'))
