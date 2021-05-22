import os

from .common import *


def fetch_cases(source: str) -> list[dict]:
    return []  # not implemented yet


def normalize_path(path: str) -> str:
    if '.' not in os.path.split(path)[-1]:
        return path + '.case.yml'
    else:
        return path


def main(args: dict) -> None:
    path = normalize_path(args['case'])
    source = args['source']
    cases = read_cases(path)
    if source is not None:
        cases.extend(fetch_cases(source))
    if not cases:
        print('For information about case files, please refer to documentation')
    write_cases(cases, path)
