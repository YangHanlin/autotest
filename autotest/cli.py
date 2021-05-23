import argparse
import sys
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
    if len(sys.argv) < 2 or not preflight_check_action(sys.argv[1]):
        sys.argv.insert(1, default_action.name)
    args = vars(init_commandline_parser().parse_args())
    dispatch_action(args)
