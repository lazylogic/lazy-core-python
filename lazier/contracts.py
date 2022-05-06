"""
Interfaces or abstract classes
"""
import importlib
from abc import ABCMeta, abstractmethod
from typing import Union

from .foundations import Dictionary


class Runnable:
    def run(self, *args, **kwargs):
        pass

    def start(self, *args, **kwargs):
        pass

    def stop(self, *args, **kwargs):
        pass


class Observable:
    _obs: set

    def add_observer(self, obj: object):
        self._obs.add(obj)

    def notify_observers(self, *args, **kwargs):
        [ob.update(self, *args, **kwargs) for ob in self._obs]


class Observer(metaclass=ABCMeta):
    @abstractmethod
    def update(self, obj: object, *args, **kwargs):
        pass


class ModuleFactory:
    __ROOT__: str = 'engine'
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
        return cls.load_class(name)(props, *args, **kwargs)

    @classmethod
    def load_class(cls, name: str):
        from .utils import upper_first
        names = name.split('.')
        if len(names) == 3:
            package = names[0]
            module = names[1]
            name = f'{upper_first(names[2])}{package.capitalize()}'
        elif len(names) == 2:
            package = cls.__PACKAGE__ or ''
            module = names[0]
            name = f'{upper_first(names[1])}{package.capitalize()}'
        else:
            package = cls.__PACKAGE__ or ''
            module = f'{upper_first(name)}{package.capitalize()}'
            name = module

        return getattr(importlib.import_module(f"{cls.__ROOT__}{f'.{package}' if package else ''}.{module}"), name)
