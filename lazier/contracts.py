"""
Interfaces or abstract classes
"""
import importlib
from multiprocessing import Queue, Manager
from typing import Union

from .foundations import Dictionary


class Runnable:
    def start(self, *args, **kwargs):
        self.run(*args, **kwargs)

    def run(self, *args, **kwargs):
        pass

    def stop(self, *args, **kwargs):
        pass


class Observable:
    _obs: set

    def add_observer(self, obj: object):
        self._obs.add(obj)

    def notify_observers(self, *args, **kwargs):
        [ob.update(self, *args, **kwargs) for ob in self._obs]


class Observer:
    def update(self, obj: object, *args, **kwargs):
        raise NotImplementedError


class Queueable:
    queue: Queue

    def __init__(self, queue: Queue = None):
        self.queue = queue or Manager().Queue()

    def mediate(self, obj):
        raise NotImplementedError


class ModuleFactory:
    __PACKAGE__: str = ''
    __MODULE__: str = ''
    __DEFAULT__: str = 'Default'

    @classmethod
    def create(cls, name: Union[str, dict] = None, props: dict = {}, *args, **kwargs):
        if name and isinstance(name, dict):
            name, props = name.get('type'), Dictionary(name).merge(props)
        elif not name and isinstance(props, dict):
            name, props = props.get('type'), props
        return cls._create(name or cls.__DEFAULT__, props, *args, **kwargs)

    @classmethod
    def _create(cls, name: str, props: dict = {}, *args, **kwargs):
        return cls.load_class(name)(props=props, *args, **kwargs)

    @classmethod
    def load_class(cls, path: str):
        from .utils import upper_first
        package = cls.__PACKAGE__.split('.') if cls.__PACKAGE__ else []
        if '.' in path:
            paths = path.split('.')
            name = paths.pop()
            module = paths.pop()
            package.extend(paths)
        else:
            name = path
            module = cls.__MODULE__
        return getattr(importlib.import_module('.'.join(package)), f'{upper_first(name)}{module.capitalize()}')


# for test
if __name__ == "__main__":
    class AFactory(ModuleFactory):
        pass
