def _handler_decorator_fabric(cls, handler_type, trigger):
    def decorator(func):
        def _wrapper(*args, **kwargs):
            func(*args, **kwargs)
        cls._handlers[handler_type][trigger] = [_wrapper] \
            if trigger not in cls._handlers[handler_type] \
            else [*cls._handlers[handler_type][trigger], _wrapper]
        return _wrapper

    return decorator


def ev(cls, event):
    return _handler_decorator_fabric(cls, 'events', event)


def msg(cls, message):
    return _handler_decorator_fabric(cls, 'messages', message)


def cmd(cls, command):
    return _handler_decorator_fabric(cls, 'commands', command)


class BaseController:
    def __init__(self):
        self._handlers = {
            'events': {},
            'messages': {},
            'commands': {},
        }

    def funcs(self):
        pass

    def get_handlers(self):
        return self._handlers