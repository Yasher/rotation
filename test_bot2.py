import telebot
from telebot import types # для указание типов
import config

bot = telebot.TeleBot(config.config['token'])




@bot.message_handler(commands=['start']) #создаем команду
def start(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("20:30 - 8:30 ", callback_data = "1")
    button2 = types.InlineKeyboardButton("8:30 - 20:30 ", callback_data = "2")
    markup.add(button1)
    markup.add(button2)
    text_button = "Выбери смены 🙈:"
    bot.send_message(message.chat.id, text_button.format(message.from_user), reply_markup=markup)
    text_button = "Вkfdjgljk;dzfhj"



@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):


    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("20:30 - 8:30 ", callback_data="1")

    markup.add(button1)

    text_button = "Выбери смены 🙈:"
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text= text_button, reply_markup=markup)

    # markup = types.InlineKeyboardMarkup()
    # print (call.data)
    # button3 = types.InlineKeyboardButton("17:00 ", callback_data="3")
    # markup.add(button3)
    # bot.send_message(message.chat.id, "Выбери смены !!!:".format(message.from_user), reply_markup=markup)
    # bot.register_next_step_handler(message, redraw)

def redraw(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("20:30 - 8:30 ", callback_data = "1")
    button2 = types.InlineKeyboardButton("8:30 - 20:30 ", callback_data = "2")
    markup.add(button1)
    markup.add(button2)
    bot.send_message(message.chat.id, "Выбери смены !!!:".format(message.from_user), reply_markup=markup)




bot.infinity_polling()
