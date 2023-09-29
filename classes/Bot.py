import telebot
from classes.MessageSession import MessageSession

def check_event_pattern_match(pattern, string) -> tuple:
    pattern_fragments = pattern.split("/")
    string_fragments = string.split("?")[0].split("/")
    values = dict()
    if len(pattern_fragments) != len(string_fragments):
        return (False, dict())

    for i in range(len(pattern_fragments)):
        pattern_fragment = pattern_fragments[i]
        string_fragment = string_fragments[i]

        if ":" in pattern_fragment:
            tp = pattern_fragment.split(":")[0]
            name = pattern_fragment.split(":")[1]

            values[name] = string_fragment

            if tp == "int":
                values[name] = int(string_fragment)
            if tp == "float":
                values[name] = float(string_fragment)
            if tp == "bool":
                values[name] = bool(string_fragment)
        else:
            if pattern_fragment != string_fragment:
                return (False, dict())

    if "?" in string:
        params = string.split("?")[1].split("&")
        for param in params:
            if "=" in param:
                name, val = param.split("=")
                values[name] = val

    return (True, values)


class Bot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.add_messages_listener()
        self._handlers = dict()

    def add_messages_listener(self):
        @self.bot.message_handler()
        def handle_message(message):
            ms = MessageSession(self, self.bot, message)
            if message.text.startswith("/"):
                cmd = message.text.split()[0].replace("/", "")
                self.trigger_command(cmd, ms=ms)
            else:
                self.trigger_message(message.text, ms=ms)

        @self.bot.callback_query_handler(lambda x: True)
        def handle_callback(call):
            ms = MessageSession(self, self.bot, call.message, from_bot=True, user=call.from_user)
            self.bot.answer_callback_query(call.id)
            self.trigger_event(call.data, ms=ms)

    # Функция для триггера ивента в обход коллбэков
    def trigger_message_event(self, event, message):
        ms = MessageSession(self, self.bot, message)
        self.trigger_event(event, ms=ms)

    # Триггеры
    def trigger(self, handler_type, trigger, *args, **kwargs):
        if handler_type in self._handlers:
            for existing_trigger in self._handlers[handler_type]:
                match = check_event_pattern_match(existing_trigger, trigger)
                if match[0]:
                    for f in self._handlers[handler_type][existing_trigger]:
                        f(*args, **match[1], **kwargs)

    def trigger_event(self, event, *args, **kwargs):
        self.trigger('events', event, *args, **kwargs)

    def trigger_message(self, message, *args, **kwargs):
        self.trigger('messages', message, *args, **kwargs)

    def trigger_command(self, command, *args, **kwargs):
        self.trigger('commands', command, *args, **kwargs)

    # Добавление ивентов контроллеров
    def add_controllers(self, controllers):
        for c in controllers:
            c.funcs()

            handlers = c.get_handlers()
            for handler_type in handlers:
                new_handlers = dict() if handler_type not in self._handlers else self._handlers[handler_type]

                for handler in handlers[handler_type]:
                    if handler in new_handlers:
                        new_handlers[handler].extend(handlers[handler_type][handler])
                    else:
                        new_handlers[handler] = [*handlers[handler_type][handler]]

                self._handlers[handler_type] = new_handlers

    def polling(self):
        self.bot.polling()