"""
Extended classes of the Python classes
"""
from enum import Enum


class Array(list):

    def __init__(self, arg=[]):
        super(Array, self).__init__(arg if isinstance(arg, list) else [arg])

    def get(self, i: int, default=None):
        return self[i] if i < len(self) else default

    def update(self, i: int, value):
        if i < len(self):
            self[i] = value

    def distinct(self):
        return Array.distinct_items(self)

    def list(self):
        try:
            return list(self)
        except:
            return []

    @staticmethod
    def distinct_items(data: list):
        distinct = []
        [(distinct.append(i) if i not in distinct else None) for i in data]
        return distinct

    @staticmethod
    def extract_values(data: list, key):
        values = []
        for item in (data or {}):
            if isinstance(item, dict):
                values.append(item.get(key))
        return values


class Dictionary(dict):
    def __init__(self, seq=None, **kwargs):
        seq = seq if seq or kwargs else {}
        super(Dictionary, self).__init__(seq, **kwargs)

    def __getattr__(self, name):
        return self.get(name)

    # def __getattr__(self, name):
    #     # v = super().__getattribute__(name) if name.startswith('__') else self.getitem(name)
    #     return self.getitem(name) if isinstance(self, Dictionary) else None
    #     # return super().__getattribute__(name) if name.startswith('__') else self.getitem(name)
    #
    # def __getstate__(self):
    #     return self.__dict__

    def __dict__(self):
        return self.dict()

    def get(self, key, default=None):
        return Dictionary.get_item(self, key, default)

    def has(self, key):
        # return key in self
        return Dictionary.has_key(self, key)

    def update(self, E=None, **F):
        super().update(E, **F)
        return self

    def merge(self, *others: dict):
        for d in others or []:
            Dictionary.merge_item(self, d if isinstance(d, dict) else {})
        return self

    def rebuild(self, *others: dict):
        for d in others or []:
            Dictionary.rebuild_item(self, d if isinstance(d, dict) else {})
        return self

    def replace(self, *others: dict):
        for d in others or []:
            Dictionary.replace_item(self, d if isinstance(d, dict) else {})
        return self

    def extract(self, *keys: str):
        return Dictionary(Dictionary.extract_item(self, *keys))

    def join(self, a: str = '&'):
        return

    def dict(self):
        try:
            return dict(self)
        except:
            return {}

    @staticmethod
    def has_key(dic: dict, path: str) -> bool:
        paths = path.split('.') if isinstance(path, str) else path
        return (paths[0] in dic if 1 == len(paths) else Dictionary.has_key(dic.get(paths[0]), paths[1:])) if isinstance(dic, dict) else False

    @staticmethod
    def get_item(dic: dict, path: str, default=None):
        from functools import reduce
        try:
            item = reduce(dict.__getitem__, path.split('.'), dic) if isinstance(path, str) else default
            item = default if item is None else item
        except:
            item = default
        finally:
            return Dictionary(item) if isinstance(item, dict) else item

    @staticmethod
    def merge_item(dic: dict, other: dict) -> dict:
        from collections.abc import Mapping
        try:
            for k, v in other.items():
                if k in dic and isinstance(dic[k], dict) and isinstance(v, Mapping):
                    Dictionary.merge_item(dic[k], v)
                elif k in dic and isinstance(dic[k], list) and isinstance(v, list):
                    dic[k].extend(v)
                    dic[k] = Array.distinct(dic[k])
                else:
                    dic[k] = v
        finally:
            return Dictionary(dic)

    @staticmethod
    def rebuild_item(dic: dict, other: dict) -> dict:
        other = Dictionary(other)
        for key, val in (dic or {}).items():
            dic[key] = other.get(f'{key}.{val}', val)
        return Dictionary(dic)

    @staticmethod
    def replace_item(dic: dict, other: dict) -> dict:
        other = Dictionary(other)
        for key, val in (dic or {}).items():
            dic[key] = other.get(val, val)
        return Dictionary(dic)

    @staticmethod
    def extract_item(dic: dict, *keys: str) -> dict:
        return Dictionary({key: dic.get(key) for key in keys} if isinstance(dic, dict) and isinstance(keys, (list, tuple)) else {})

    @staticmethod
    def from_list(data: list, key: str) -> dict:
        try:
            return Dictionary({str(i.get(key)): i for i in data} if isinstance(data, list) else {})
        except Exception as e:
            return Dictionary()

    @staticmethod
    def join(dic: dict, separator: str = '&', delimiter: str = '=', prefix: str = '', suffix: str = ''):
        return f"{prefix}{separator.join(delimiter.join((key, val)) for (key, val) in dic.items())}{suffix}" if dic and isinstance(dic, dict) else ''


class XEnum(Enum):
    pass


# for test
if __name__ == "__main__":
    d = Dictionary({'@a': 1, 'b': 2, 'c': {'d': {'e': ['a', 'b', 'c']}}})
    print(d.has('c.d.e.a'))
    print(d.extract('a', 'b', 'c'))
