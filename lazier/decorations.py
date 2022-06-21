"""
Decorations
"""
import logging

from .foundations import Dictionary


def Singleton(cls):
    cls_init = cls.__init__

    def __new__(cls: object, *args, **kwargs):
        if not (hasattr(cls, '_instance') and isinstance(cls._instance, cls)):
            cls._instance = object.__new__(cls)
            cls._is_init = False
        return cls._instance

    def __init__(self, *args, **kwargs):
        cls = type(self)
        if not cls._is_init:
            cls_init(self, *args, **kwargs)
            cls._is_init = True

    cls.__new__ = __new__
    cls.__init__ = __init__
    return cls


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
