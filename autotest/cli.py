import argparse


def init_commandline_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(metavar='action', help='action to take',
                                       dest='action', required=True)

    run_parser = subparsers.add_parser('run', aliases=['r'],
                                       help='run command and judge the results against cases')
    run_parser.add_argument('command',
                            help='command to run')
    run_parser.add_argument('-c', '--case', required=False,
                            help='file to read cases from; defaults to <command>.case.yml')
    run_parser.add_argument('-r', '--allow-runtime-error', required=False, action='store_true',
                            help='allow runtime errors (in which command exits with non-zero code)')

    generate_parser = subparsers.add_parser('generate', aliases=['gen', 'g'],
                                            help='generate empty test case file or fetch from OJ')
    generate_parser.add_argument('case',
                                 help='case file to generate; suffix \'.case.yml\' will be appended if '
                                      'no extension is provided')
    generate_parser.add_argument('-s', '--source', required=False,
                                 help='source to fetch cases from, e.g. luogu/p1001')

    return parser


def main() -> None:
    parsing_results = vars(init_commandline_parser().parse_args())
    print('parsing results =', parsing_results)
