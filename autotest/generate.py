import yaml
import os

EMPTY_CASE = {
    'input': '1 1',
    'output': '2',
}


def fetch_cases(source: str) -> list[dict]:
    return [EMPTY_CASE]  # Not implemented yet


def write_cases(cases: list[dict], path: str) -> None:
    if '.' not in os.path.split(path)[-1]:
        path = path + '.case.yml'

    with open(path, 'w') as file:
        file.write(yaml.dump({
            'cases': cases,
        }))


def main(args: dict) -> None:
    if args['source'] is None:
        cases = [EMPTY_CASE]
    else:
        cases = fetch_cases(args['source'])

    write_cases(cases, args['case'])
