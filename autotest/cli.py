import argparse
import sys

from . import run, generate


actions = [
    run.commandline_action,
    generate.commandline_action,
]
default_action = actions[0]


def init_application() -> None:
    pass


def init_commandline_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(metavar='action', help='action to take',
                                       dest='action', required=True)
    for action in actions:
        action_parser = subparsers.add_parser(name=action.name, aliases=action.aliases, help=action.help)
        action.parser_handler(action_parser)
    return parser


def preflight_check_action(arg: str) -> bool:
    for action in actions:
        if arg == action.name or arg in action.aliases:
            return True
    return False


def dispatch_action(args: dict) -> None:
    action = args.pop('action')
    if action in ('run', 'r'):
        run.main(args)
    elif action in ('generate', 'gen', 'g'):
        generate.main(args)
    else:
        raise NotImplementedError('Action {} is not implemented yet'.format(action))


def main() -> None:
    init_application()
    if len(sys.argv) < 2 or not preflight_check_action(sys.argv[1]):
        sys.argv.insert(1, default_action.name)
    args = vars(init_commandline_parser().parse_args())
    dispatch_action(args)
