class CommandHandler:
    def __init__(self):
        self._handlers = {}

    def register(self, command_class):
        def decorator(handler_func):
            self._handlers[command_class] = handler_func
            return handler_func
        return decorator

    def handle(self, command):
        handler_func = self._handlers[type(command)]
        return handler_func(command)
