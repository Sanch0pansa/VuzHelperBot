from classes import Bot
from controllers.WelcomeController import WelcomeController
import os
from dotenv import load_dotenv

wc = WelcomeController()

load_dotenv()
bot = Bot.Bot(os.environ.get('TOKEN'))
bot.add_controllers([wc])
bot.polling()