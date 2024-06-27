#age = 66

#print ("hkjdfghk" + str(age) +"jfadh")

import telebot
from telebot import types # для указание типов
import config
#import config
import config
import db


bot = telebot.TeleBot(config.config['token'])




#@bot.message_handler(commands=['start', 'help'])

@bot.message_handler(commands=['start']) #создаем команду
#def send_welcome(message):
#	bot.reply_to(message, "Howdy, how are you doing?")
def start(message):
    tg_id = message.from_user.id
    if db.get_user_role(tg_id) == True:
        rkm = types.ReplyKeyboardMarkup()
        rkm.add(types.KeyboardButton("Период"))
        msg = bot.send_message(message.chat.id, "тутуту", reply_markup=rkm)
    else:
        bot.send_message(chat_id=message.chat.id, text=";fkdjgksdfgl;k")

    #msg = bot.send_message(message.chat.id, "Запись данных...")
    #bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text="Данные записаны!!!")

bot.infinity_polling(none_stop=True)