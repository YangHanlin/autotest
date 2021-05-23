from typing import Callable, Union


class CommandlineAction:
    def __init__(self, name: str, parser_handler: Callable, main_handler: Callable,
                 aliases: Union[list[str], None] = None, help: str = ''):
        self.name = name
        self.parser_handler = parser_handler
        self.main_handler = main_handler
        self.aliases = aliases
        self.help = help
