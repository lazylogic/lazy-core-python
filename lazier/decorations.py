"""
Decorations
"""
import logging

from lazier import Dictionary


def Singleton(cls):
    class Wrapper(cls):
        _instance = None

        def __new__(cls, *args, **kwargs):
            if Wrapper._instance is None:
                Wrapper._instance = super(Wrapper, cls).__new__(cls, *args, **kwargs)
                Wrapper._instance._sealed = False
            return Wrapper._instance

        def __init__(self, *args, **kwargs):
            if not self._sealed:
                super(Wrapper, self).__init__(*args, **kwargs)
                self._sealed = True

    Wrapper.__name__ = cls.__name__
    return Wrapper


def Logging(multiprocess: bool = False):
    def getLogger(name: str, multiprocess: bool):
        if multiprocess:
            import multiprocessing
            log = multiprocessing.get_logger()
            log.propagate = True
        else:
            log = logging.getLogger(name)
        return log

    def wrapper(cls):
        cls_init = cls.__init__

        def __init__(self, *args, **kwargs):
            # self.log = getLogger(multiprocess)
            # self.log = logging.getLogger(self.__class__.__name__)
            if multiprocess:
                import multiprocessing
                self.log = multiprocessing.get_logger()
                self.log.propagate = True
            else:
                self.log = logging.getLogger(self.__class__.__name__)
            cls_init(self, *args, **kwargs)

        cls.__init__ = __init__
        return cls

    return wrapper(multiprocess) if isinstance(multiprocess, type) else wrapper


def HasProperties(cls):
    cls_init = cls.__init__

    def __init__(self, props: dict = {}, *args, **kwargs):
        self.props = Dictionary(getattr(self, 'default', {})).merge(getattr(self, 'preset', {}), props or {})
        self.debug = self.props.get('debug', False)
        cls_init(self, *args, **kwargs)

    cls.__init__ = __init__
    return cls
