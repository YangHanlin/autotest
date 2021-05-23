import yaml
from pathlib import Path
from typing import Union


class Case:
    def __init__(self, input: str = '', output: str = '', timeout: Union[float, None] = None):
        self.input = input
        self.output = output
        self.timeout = timeout

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def to_dict(self):
        return {
            'input': self.input,
            'output': self.output,
            'timeout': self.timeout,
        }


def read_case_file(path: Union[str, Path], allow_nonexistent_file: bool = True) -> list[Case]:
    try:
        with open(path, 'r') as file:
            # use of yaml.BaseLoader is intentional and considers all scalars as strings
            case_structure = yaml.load(file.read(), yaml.BaseLoader)
            cases = list(map(Case.from_dict, case_structure['cases']))
            return cases
    except FileNotFoundError as err:
        if allow_nonexistent_file:
            return []
        else:
            raise err


def write_case_file(cases: list[Case], path: Union[str, Path]) -> None:
    with open(path, 'w') as file:
        case_structure = {
            'cases': list(map(Case.to_dict, cases)),
        }
        file.write(yaml.dump(case_structure, default_flow_style=False))
