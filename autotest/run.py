import subprocess
import time

from .common import *


def main(args: dict) -> None:
    command = args['command']
    case_path = args['case'] or command + '.case.yml'
    allow_runtime_error = args['allow_runtime_error']

    try:
        cases = read_cases(case_path, allow_nonexistent_file=False)
    except FileNotFoundError as err:
        raise err  # TODO: replace with universal error handling mechanisms

    total = len(cases)
    stats = {
        'AC': 0,
        'WA': 0,
        'RE': 0,
    }
    for i, case in enumerate(cases):
        print('Case #{}: '.format(i + 1), end='')
        case_input, case_output = map(str, [case['input'], case['output']])
        timestamp_start = time.time()
        proc = subprocess.run(command, input=case_input, capture_output=True, shell=True, text=True)
        timestamp_end = time.time()
        if not allow_runtime_error and proc.returncode != 0:
            stats['RE'] += 1
            print('RE ', end='')
        elif proc.stdout.strip() == case_output.strip():
            stats['AC'] += 1
            print('AC ', end='')
        else:
            stats['WA'] += 1
            print('WA ', end='')
        print(str(timestamp_end - timestamp_start) + 's')

    print(stats)
