import re
from re import Pattern
from typing import Union

from lazier.foundations import Dictionary, Array
from lazier.utils import load_properties, yml_path


def properties(*props: dict, include_path: str = None, replace: bool = True) -> Dictionary:
    return Properties().parse(*props, include_path=include_path, replace=replace)


class Properties:
    REPLACE_PATTERN: Pattern = re.compile(r'\${([\w\.\s:]+)}')

    p: dict
    include_path: str

    @classmethod
    def load(cls, ctx: Union[str, dict]) -> dict:
        return load_properties(ctx)

    def parse(self, *props: dict, include_path: str = None, replace: bool = True) -> Dictionary:
        props = [self.load(prop) for prop in props]
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
                for match in re.findall(self.REPLACE_PATTERN, str(value)) or []:
                    values = Array(match.split(":"))
                    renewal = self.props.get(values.get(0), values.get(1))
                    return replace(value.replace(f"${{{match}}}", renewal))
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


# for test
if __name__ == "__main__":
    ptn = re.compile(r'\${(.+)}')
    m = re.search(ptn, '${a}${b}')
    print(m)
