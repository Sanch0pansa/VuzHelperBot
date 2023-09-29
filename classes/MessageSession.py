

class MessageSession:
    def __init__(self, bot_object, bot, message, from_bot=False, user=None):
        self.bot = bot
        self.bot_object = bot_object
        self.message = message
        self.from_bot = from_bot
        self.user = user if user else self.message.from_user

    def send(self, text, *args, **kwargs):
        self.bot.send_message(
            chat_id=self.message.chat.id,
            text=text,
            * args,
            **kwargs,

        )

    def reply(self, text, *args, **kwargs):
        self.bot.send_message(self.message.chat.id, text,  reply_to_message_id=self.message.id, *args, **kwargs)

    def next_msg_ev(self, event, *args, **kwargs):
        self.bot.register_next_step_handler(self.message,
                                            lambda message: self.bot_object.trigger_message_event(event,
                                                                                                  message,
                                                                                                  *args,
                                                                                                  **kwargs
                                                                                                  ))

    def replace_msg(self, text, *args, **kwargs):
        self.bot.edit_message_text(
            chat_id=self.message.chat.id,
            text=text,
            message_id=self.message.message_id,
            *args,
            **kwargs)

    def send_or_replace(self, *args, **kwargs):
        if self.from_bot:
            self.replace_msg(*args, **kwargs)
        else:
            self.send(*args, **kwargs)

    def trigger_event(self, event, *args, **kwargs):
        self.bot_object.trigger_message_event(event, self.message, *args, **kwargs)

