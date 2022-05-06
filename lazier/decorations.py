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
    def wrapper(cls):
        cls_init = cls.__init__

        def __init__(self, *args, **kwargs):
            # self.log = get_logger(self.__class__.__name__, multiprocess)
            self.log = logging.getLogger(self.__class__.__name__)
            cls_init(self, *args, **kwargs)

        cls.__init__ = __init__
        return cls

    return wrapper(multiprocess) if isinstance(multiprocess, type) else wrapper


def HasProperties(cls):
    cls_init = cls.__init__

    def __init__(self, props: dict = {}, *args, **kwargs):
        self.props = Dictionary(getattr(self, 'preset', {})).merge(props)
        self.debug = self.props.get('debug', False)
        cls_init(self, *args, **kwargs)

    cls.__init__ = __init__
    return cls
