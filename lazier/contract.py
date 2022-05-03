"""
Interfaces or abstract classes
"""
from abc import ABCMeta, abstractmethod


class Observable(metaclass=ABCMeta):
    _obs: set

    def add_observer(self, obj: object):
        self._obs.add(obj)

    def notify_observers(self, *args, **kwargs):
        [ob.update(self, *args, **kwargs) for ob in self._obs]


class Observer(metaclass=ABCMeta):
    @abstractmethod
    def update(self, obj: object, *args, **kwargs):
        pass

# class AbstractFactory:
#
#     @classmethod
#     def create(cls, *args, **kwargs):
#         pass
#
#     @classmethod
#     def _create(cls, module: str, props: dict, default: str = ''):
#         return cls._load_class(module, props.get('type'), default)(props)
#
#     @classmethod
#     def _load_class(cls, module: str, name: str, default: str = ''):
#         from core.utils import load_class
#         return load_class(cls._class_path(module, name, default))
#
#     @classmethod
#     def _class_path(cls, module: str, name: str, default: str = ''):
#         return f"{cls._module_path(module)}.{cls._class_name(name, default)}{cls._class_suffix(module)}"
#
#     @classmethod
#     def _module_path(cls, module: str):
#         return (module or '').lower()
#
#     @classmethod
#     def _class_name(cls, name: str, default: str = ''):
#         from core.utils import upper_first
#         return upper_first(name or default)
#
#     @classmethod
#     def _class_suffix(cls, module: str):
#         return str(module).split('.')[-1].capitalize()
