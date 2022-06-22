import logging
import os
from logging import config
from typing import Union

from lazier.properties import properties
from lazier.utils import load_properties


class Logger:
    @classmethod
    def configuration(cls, conf: Union[str, dict], level: Union[int, str] = logging.DEBUG, filepath: str = 'service'):
        try:
            conf = properties(
                load_properties(conf),
                {"logging": {"level": level}} if level else {},
                {"logging": {"filename": os.path.basename(filepath)}} if filepath else {},
            )
            log_path = os.path.dirname(filepath or '')
            if conf.has('handlers.file.filename'):
                conf['handlers']['file']['filename'] = f"{log_path}/{conf.get('handlers.file.filename')}"
            if conf.has('handlers.rotating.filename'):
                conf['handlers']['rotating']['filename'] = f"{log_path}/{conf.get('handlers.rotating.filename')}"
            logging.config.dictConfig(conf)
        except Exception as e:
            logging.getLogger().exception(e)


# for test
if __name__ == "__main__":
    print(os.path.basename('/abc.ddd'))
