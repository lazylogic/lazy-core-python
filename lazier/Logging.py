import logging
import os
from typing import Union

from lazier.properties import properties
from lazier.utils import load_properties


class Logging:
    @classmethod
    def configuration(cls, conf: Union[str, dict], level: Union[int, str] = logging.DEBUG, filepath: str = 'service'):
        try:
            config = properties(
                load_properties(conf),
                {"logging": {"level": level}} if level else {},
                {"logging": {"filename": os.path.basename(filepath)}} if filepath else {},
            )
            log_path = os.path.dirname(filepath or '')
            if config.has('handlers.file.filename'):
                config['handlers']['file']['filename'] = f"{log_path}/{config.get('handlers.file.filename')}"
            if config.has('handlers.rotating.filename'):
                config['handlers']['rotating']['filename'] = f"{log_path}/{config.get('handlers.rotating.filename')}"
            logging.config.dictConfig(config)
        except Exception as e:
            logging.getLogger().exception(e)


# for test
if __name__ == "__main__":
    print(os.path.basename('/abc.ddd'))
