from classes import Bot
from controllers.UserController import UserController
import os
from dotenv import load_dotenv

uc = UserController()

load_dotenv()
bot = Bot.Bot(os.environ.get('TOKEN'))
bot.add_controllers([uc])
bot.polling()