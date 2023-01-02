from typing import Any


class Command:
    """
    Defines a Command interface that all commands in the application should implement.
    """
    def get_name(self) -> str:
        raise NotImplementedError()


class CommandHandler:
    """
    Define a CommandHandler interface that all command handlers in the application should implement.
    """
    def handle(self, command: Command) -> Any:
        raise NotImplementedError()


class CommandBus:
    """
     CommandBus is responsible for dispatching commands to the appropriate command handler
    """
    def register_handler(self, command_name: str, handler: CommandHandler):
        pass

    def dispatch(self, command: Command) -> Any:
        pass

