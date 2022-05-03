import importlib
import json
import logging
import os

import yaml


def is_empty(val) -> bool:
    return val if isinstance(val, bool) else val is None or len(val) == 0


def upper_first(string: str):
    for i in range(0, len(string)):
        if string[i].isalpha():
            return string[:i + 1].upper() + string[i + 1:]
    return string


def mkdir(path: str, refresh: bool = None):
    if os.path.exists(path) and refresh:
        import shutil
        shutil.rmtree(path)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def file_path(filename: str, ext: str, path: str = None):
    import re
    filename = filename.strip()
    name, ex = os.path.splitext(filename)
    match = re.match(r'^(file://)(.+)', filename, re.I)
    return (match[2] if match else f"{path}/{name}") + (ex or f'.{ext}')


def json_path(filename: str, path: str = None):
    return file_path(filename, 'json', path)


def yml_path(filename: str, path: str = None):
    return file_path(filename, 'yml', path)


def load_file(path: str) -> str:
    with open(path) as file:
        return file.read()


def load_json(ctx: str) -> dict:
    """
    Read json file or pars json string.

    :param ctx: json file or json string
    :return: dict
    """
    try:
        if os.path.isfile(ctx):
            with open(ctx) as file:
                return json.load(file)
        else:
            return json.loads(ctx)
    except Exception as e:
        logging.exception(e)
        return {}


def load_yml(ctx: str) -> dict:
    """
    Read yml file or pars yml string.

    :param ctx: yml file or yml string
    :return: dict
    """
    try:
        if os.path.isfile(ctx):
            with open(ctx) as file:
                return yaml.load(file, Loader=yaml.FullLoader)
        else:
            return yaml.safe_load(ctx)
    except Exception as e:
        logging.exception(e)
        return {}


def load_properties(ctx: str) -> dict:
    """
    Read json or yml file or pars json or yml string.

    :param ctx: json or yml file or json or yml string.
    :return: dict
    """
    try:
        if isinstance(ctx, dict):
            return ctx

        path, ext = os.path.splitext(ctx)
        if ctx.startswith('{') or (ext and 'JSON' == ext[-4:].upper()):
            return load_json(ctx)

        if not ext or ('YML' == ext[-3:].upper() or 'YAML' == ext[-4:].upper()):
            return load_yml(path + ext)
    except Exception as e:
        logging.exception(e)
        return {}


def load_class(module: str, name: str):
    return getattr(importlib.import_module(module), name)


def sp(o, sort_keys=False, indent=2):
    from pprint import pformat
    try:
        return json.dumps(o, sort_keys=sort_keys, indent=indent, ensure_ascii=False, default=lambda a: vars(a))
    except TypeError as e:
        return pformat(vars(o), indent=indent)
    except Exception as e:
        return str(o)


def pp(o, sort_keys=False, indent=2):
    print(sp(o, sort_keys, indent))


def delay(min_: int = 0, max_: int = 0):
    import time, random
    min_ = abs(min_ or 0)
    max_ = max(min_, abs(max_ or 0))
    if min_ < max_:
        time.sleep(random.randrange(min_, max_))
    elif 0 < max_:
        time.sleep(random.randrange(max_ - 1, max_))


# TODO: *args
def concoct(one: list, other: list, separator=', ', delimiter=':'):
    return separator.join([f'{x}{delimiter}{y}' for x, y in zip(one or [], other or []) if x != '' and y != ''])


def hashing(o):
    import copy
    if isinstance(o, dict):
        new_o = copy.deepcopy(o)
        for k, v in new_o.items():
            new_o[k] = hashing(v)
        return hash(tuple(frozenset(sorted(new_o.items()))))
    if isinstance(o, (set, tuple, list)):
        return hash([hashing(e) for e in o])
    else:
        return hash(o)
