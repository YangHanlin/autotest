import os
import logging
import argparse

from .internal.case import *
from .internal.commandline_action import CommandlineAction

logger = logging.getLogger()


def fetch_cases(source: str) -> list[Case]:
    return []  # not implemented yet


def normalize_path(path: str) -> str:
    if '.' not in os.path.split(path)[-1]:
        return path + '.case.yml'
    else:
        return path


def main(args: dict) -> None:
    path = normalize_path(args['case'])
    source = args['source']
    cases = read_case_file(path)
    if source is not None:
        cases.extend(fetch_cases(source))
    if not cases:
        print(logger.getEffectiveLevel())
        logger.info('For information about case files, please refer to documentation')
    write_case_file(cases, path)


def init_parser(parser: argparse.ArgumentParser):
    parser.add_argument('case',
                        help='case file to generate; suffix \'.case.yml\' will be appended if '
                             'no extension is provided')
    parser.add_argument('-s', '--source', required=False,
                        help='source to fetch cases from, e.g. luogu/p1001')


commandline_action = CommandlineAction(name='generate',
                                       parser_handler=init_parser,
                                       main_handler=main,
                                       aliases=['gen', 'g'],
                                       help='generate empty test case file or fetch from OJ')
