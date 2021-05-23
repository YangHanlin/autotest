import subprocess
import sys
import time
import argparse
from simple_chalk import chalk

from .internal.case import *
from .internal.commandline_action import CommandlineAction
from .internal.judging import TrivialJudger


def main(command: str, case_path: Union[str, None], allow_nonzero: bool) -> None:
    if case_path is None:
        case_path = command + '.case.yml'

    try:
        cases = read_case_file(case_path, allow_nonexistent_file=False)
    except FileNotFoundError as err:
        raise err  # TODO: replace with universal error handling mechanisms

    judger = TrivialJudger({
        'allow_nonzero': allow_nonzero,
    })
    total = len(cases)

    for i, case in enumerate(cases):
        print('Case {}/{}'.format(i + 1, total), end='')
        start_time = time.time()
        proc = subprocess.run(command, shell=True, text=True, input=case.input, capture_output=True)
        end_time = time.time()
        duration = end_time - start_time
        print(' ({:.3f}s): '.format(duration), end='')
        result = judger.judge(case, proc.stdout, duration, proc.returncode)
        print(result.status)
        if result.show_diff:
            expected_output = case.output
            if expected_output.endswith('\n'):
                expected_output = chalk.bgGreen(expected_output)
            else:
                expected_output = chalk.bgGreen(expected_output) + ' EOF\n'
            actual_output = proc.stdout
            if actual_output.endswith('\n'):
                actual_output = chalk.bgRed(actual_output)
            else:
                actual_output = chalk.bgRed(actual_output) + ' EOF\n'
            print(actual_output + expected_output, end='')
        print(proc.stderr, file=sys.stderr, end='')

    print('\nStatistics:')
    stats = judger.get_stats()
    max_length = max(map(len, stats.keys()))
    for stat in stats:
        print('{key:{max_length}} = {value} ({percentage:.1f}%)'.format(
            key=stat,
            value=stats[stat],
            max_length=max_length,
            percentage=stats[stat] / total * 100.0
        ))


def init_parser(parser: argparse.ArgumentParser):
    parser.add_argument('command',
                        help='command to run')
    parser.add_argument('-c', '--case-path', required=False,
                        help='file to read cases from; defaults to <command>.case.yml')
    parser.add_argument('-z', '--allow-nonzero', required=False, action='store_true',
                        help='allow programs to exit with non-zero code; otherwise it will be considered '
                             'as a runtime error (RE)')


commandline_action = CommandlineAction(name='run',
                                       parser_handler=init_parser,
                                       main_handler=main,
                                       aliases=['r'],
                                       help='run command and judge the results against cases')
