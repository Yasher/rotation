
import telebot
from telebot import types # для указание типов
#import config
import config
bot = telebot.TeleBot(config.config['token'])

#@bot.message_handler(commands=['start', 'help'])

@bot.message_handler(commands=['start'])
def start(message):
  user_id = message.from_user.id
  print(user_id)

bot.infinity_polling(none_stop=True)