import os
import logging
import argparse

from .internal.case import *
from .internal.commandline_action import CommandlineAction
from .internal import fetching
from .internal.fetching import UnsupportedSourceError

logger = logging.getLogger(__name__)


def fetch_cases(source: str) -> list[Case]:
    fetch = None
    for handler in fetching.handlers:
        try:
            logger.debug('trying with fetch handler {}'.format(handler.__name__))
            fetch = handler(source)
        except UnsupportedSourceError:
            pass
        else:
            break
    if fetch is None:
        logger.warning('source {} is not currently supported'.format(source))
        return []
    logger.debug('using handler {}'.format(handler.__name__))
    return fetch.get()


def normalize_path(path: str) -> str:
    if '.' not in os.path.split(path)[-1]:
        return path + '.case.yml'
    else:
        return path


def main(case_path: str, source: Union[str, None]) -> None:
    if '.' not in os.path.split(case_path)[-1]:
        case_path = case_path + '.case.yml'
    cases = read_case_file(case_path)
    if source is not None:
        cases.extend(fetch_cases(source))
    if not cases:
        logger.info('seemingly an empty case file was generated; see documentation for case file format')
    write_case_file(cases, case_path)


def init_parser(parser: argparse.ArgumentParser):
    parser.add_argument('case_path',
                        help='case file to generate; suffix \'.case.yml\' will be appended if '
                             'no extension is provided')
    parser.add_argument('-s', '--source', required=False,
                        help='source to fetch cases from, e.g. https://www.luogu.com.cn/problem/UVA100')


commandline_action = CommandlineAction(name='generate',
                                       parser_handler=init_parser,
                                       main_handler=main,
                                       aliases=['gen', 'g'],
                                       help='generate empty test case file or fetch from OJ')
