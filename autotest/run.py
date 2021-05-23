import subprocess
import time
import argparse

from .internal.case import *
from .internal.commandline_action import CommandlineAction


def main(command: str, case_path: Union[str, None], allow_runtime_error: bool) -> None:
    if case_path is None:
        case_path = command + '.case.yml'

    try:
        cases = read_case_file(case_path, allow_nonexistent_file=False)
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
        case_input, case_output = map(str, [case.input, case.output])
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


def init_parser(parser: argparse.ArgumentParser):
    parser.add_argument('command',
                        help='command to run')
    parser.add_argument('-c', '--case-path', required=False,
                        help='file to read cases from; defaults to <command>.case.yml')
    parser.add_argument('-r', '--allow-runtime-error', required=False, action='store_true',
                        help='allow runtime errors (in which command exits with non-zero code)')


commandline_action = CommandlineAction(name='run',
                                       parser_handler=init_parser,
                                       main_handler=main,
                                       aliases=['r'],
                                       help='run command and judge the results against cases')
