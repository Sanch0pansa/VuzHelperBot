from classes.BaseController import BaseController, cmd #ev, msg
# from funcs.markup_parser import view, prepare_markup


class WelcomeController(BaseController):
    def funcs(self):
        @cmd(self, 'start')
        def handle_start_command(ms):
            ms.send("Добрый день!")


