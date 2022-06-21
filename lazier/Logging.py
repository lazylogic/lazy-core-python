import logging
import os
from typing import Union

from lazier.properties import properties
from lazier.utils import load_properties, mkdir


class Logging:
    @classmethod
    def configuration(cls, conf: Union[str, dict], level: Union[int, str] = logging.DEBUG, path: str = None, filename: str = None):
        try:
            config = properties(
                load_properties(conf),
                {"logging": {"level": level}} if level else {},
                {"logging": {"filename": os.path.basename(filename)}} if filename else {},
            )
            log_path = cls.path(config.get('log_path', 'logs'), path or os.path.dirname(filename or ''))
            if config.has('handlers.file.filename'):
                config['handlers']['file']['filename'] = f"{log_path}/{config.get('handlers.file.filename')}"
            if config.has('handlers.rotating.filename'):
                config['handlers']['rotating']['filename'] = f"{log_path}/{config.get('handlers.rotating.filename')}"
            logging.config.dictConfig(config)
        except Exception as e:
            logging.getLogger().exception(e)

    @classmethod
    def path(cls, path: str = 'logs', base: str = ''):
        return mkdir(path if str(path).startswith('/') else f"{base}/{path}")


# for test
if __name__ == "__main__":
    print(os.path.basename('/abc.ddd'))
