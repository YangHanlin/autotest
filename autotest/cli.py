import argparse
import sys
import os
import logging

from . import run, generate


actions = [
    run.commandline_action,
    generate.commandline_action,
]
available_root_args = [
    '-h',
    '--help',
]
default_action = actions[0]

logger = logging.getLogger(__name__)


def init_application() -> None:
    logging.basicConfig(level=logging.INFO, style='{', format='{name}: {levelname}: {message}')


def init_commandline_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(metavar='action', help='action to take',
                                       dest='action', required=True)
    for action in actions:
        action_parser = subparsers.add_parser(name=action.name, aliases=action.aliases, help=action.help)
        action.parser_handler(action_parser)
    return parser


def preflight_check_action(arg: str) -> bool:
    if arg in available_root_args:
        return True
    for action in actions:
        if arg == action.name or arg in action.aliases:
            return True
    return False


def dispatch_action(args: dict) -> None:
    action_name = args.pop('action')
    main_handler = None
    for action in actions:
        if action_name == action.name or action_name in action.aliases:
            main_handler = action.main_handler
            break
    if main_handler is None:
        raise NotImplementedError
    return main_handler(**args)


def main() -> None:
    init_application()
    raw_args = sys.argv[1:]
    if 'AUTOTEST_DEVELOPMENT' in os.environ:
        logger.info('development mode has been enabled')
        while True:
            logger.info('current args ({}) are: {}; enter to continue or type new args'.format(len(raw_args), ', '.join(repr(raw_arg) for raw_arg in raw_args)))
            new_command = input('>')
            if not new_command.strip():
                break
            raw_args = new_command.split()
    if not raw_args or not preflight_check_action(raw_args[0]):
        raw_args.insert(0, default_action.name)
    args = vars(init_commandline_parser().parse_args(raw_args))
    dispatch_action(args)


if __name__ == '__main__':
    main()
