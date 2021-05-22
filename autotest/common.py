import yaml
from pathlib import Path
from typing import Union


def read_cases(path: Union[str, Path], allow_nonexistent_file: bool = True) -> list[dict]:
    try:
        with open(path, 'r') as file:
            # use of yaml.BaseLoader is intentional and considers all scalars as strings
            case_structure = yaml.load(file.read(), yaml.BaseLoader)
            return case_structure['cases']
    except FileNotFoundError as err:
        if allow_nonexistent_file:
            return []
        else:
            raise err


def write_cases(cases: list[dict], path: Union[str, Path]) -> None:
    with open(path, 'w') as file:
        file.write(yaml.dump({
            'cases': cases,
        }))
