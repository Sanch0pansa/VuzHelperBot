from classes.BaseController import BaseController, cmd, ev, msg
from services.db import User, Group
from funcs.markup_parser import view, prepare_markup


# Decorator, that provides user data as argument. If user is not registered, it does registrate user.
def with_user(registrate=False):
    def decorator(func):
        def _wrapper(ms, *args, **kwargs):
            telegram_id = ms.user.id

            # Trying to get user from database
            user = User.get_by_telegram_id(telegram_id)
            if not user:
                User.create({
                    'name': "",
                    'telegram_id': telegram_id,
                    'username': ms.message.from_user.username
                })
                user = User.get_by_telegram_id(telegram_id)
            func(ms, *args, user=user, **kwargs)

        return _wrapper

    return decorator


class UserController(BaseController):
    def funcs(self):
        @cmd(self, 'start')
        @with_user(True)
        def handle_start_command(ms, user=None):
            ms.send(**view("./templates/hello.xml", {'username': user[1], 'group': None}))
            ms.send_or_replace(**view("./templates/menu.xml", {}))

        @ev(self, 'menu/')
        @with_user(True)
        def handle_menu(ms, user=None):
            ms.send_or_replace(**view("./templates/menu.xml", {}))

        @ev(self, 'my_groups/')
        @with_user(True)
        def my_groups(ms, user=None):
            groups = Group.get_all_groups_by_user(user[0])
            ms.send_or_replace(**view("./templates/my_groups.xml", {'groups': groups}))

        @ev(self, 'elder_menu/')
        @with_user(True)
        def my_groups(ms, user=None):
            groups = Group.get_all_groups_by_elder(user[0])
            print(user)
            ms.send_or_replace(**view("./templates/elder_menu.xml", {'groups': groups}))

        @ev(self, 'new_group/')
        def my_groups(ms):
            ms.send("Введите имя группы:")
            ms.next_msg_ev('create_group/')

        @ev(self, 'create_group/')
        @with_user(True)
        def my_groups(ms, user=None):
            Group.create(user[0], ms.message.text)
            ms.send("Группа создана!")
            groups = Group.get_all_groups_by_elder(user[0])
            ms.send_or_replace(**view("./templates/elder_menu.xml", {'groups': groups}))




