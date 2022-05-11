import re
from re import Pattern

from .foundations import Dictionary, Array
from .utils import load_properties, yml_path


def properties(*props: dict, include_path: str = None, replace: bool = True) -> Dictionary:
    return Properties().parse([load_properties(prop) for prop in props], include_path=include_path, replace=replace)


class Properties:
    REPLACE_PATTERN: Pattern = re.compile(r'\${(.+)}')

    props: dict
    include_path: str

    def parse(self, *props: dict, include_path: str = None, replace: bool = True) -> Dictionary:
        self.include_path = include_path
        self._merge(*props)
        self._parse(self.props)
        replace and self._replace(self.props)
        return self.props

    def _merge(self, *props: dict):
        self.props, *more = props or ({}, {})
        self.props = Dictionary(self.props if isinstance(self.props, dict) else {}).merge(*more)

    def _parse(self, props: dict):

        def split(key: str, val):
            keys = key.split('.', 1)
            return {keys[0]: split(keys[1], val)} if len(keys) > 1 else {key: val}

        if isinstance(props, dict):
            for key in list(props):
                if '.' in key:
                    props.update(Dictionary(props).merge(self._parse(split(key, props[key]))))
                    props.pop(key, None)
                elif 'INCLUDE' == key.upper() and isinstance(props[key], str):
                    self._include(props, key)
                else:
                    self._parse(props[key])
            return Dictionary(props)
        else:
            return props

    def _include(self, props: dict, key: str):
        try:
            props.update(self._parse(load_properties(yml_path(props[key], self.include_path))).merge(props))
            props.pop(key, None)
        finally:
            return props

    def _replace(self, props: dict):
        def replace(value):
            try:
                if match := re.search(self.REPLACE_PATTERN, str(value)):
                    values = Array(match[1].split(":"))
                    renewal = self.props.get(values.get(0), values.get(1))
                    return replace(renewal if match[0] == value else self.REPLACE_PATTERN.sub(str(renewal), value))
                else:
                    return value
            except Exception:
                return value

        try:
            if isinstance(props, dict):
                for key, prop in props.items():
                    if isinstance(prop, str):
                        props[key] = replace(prop)
                    else:
                        self._replace(prop)
            elif isinstance(props, list):
                for prop in props:
                    self._replace(prop)
        finally:
            return props
