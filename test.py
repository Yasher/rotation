#age = 66

#print ("hkjdfghk" + str(age) +"jfadh")

import telebot
from telebot import types # для указание типов
import config
#import config
import config
import db
import voting


bot = telebot.TeleBot(config.config['token'])




#@bot.message_handler(commands=['start', 'help'])

@bot.message_handler(commands=['start']) #создаем команду
#def send_welcome(message):
#	bot.reply_to(message, "Howdy, how are you doing?")
def start(message):
    tg_id = message.from_user.id
    if db.get_user_role(tg_id) == True:
        rkm = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 3)
        rkm.add(types.KeyboardButton("Период"), types.KeyboardButton("Выборы"), types.KeyboardButton("Запись \n результатов"), types.KeyboardButton("Подмена"))
        msg = bot.send_message(message.chat.id, "Вы администратор", reply_markup=rkm)
        bot.register_next_step_handler(msg, user_handler)

    else:
        bot.send_message(chat_id=message.chat.id, text=";fkdjgksdfgl;k")

    #msg = bot.send_message(message.chat.id, "Запись данных...")
    #bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text="Данные записаны!!!")
def user_handler (message):
    if (message.text == "Период"):
        msg = bot.send_message(message.chat.id, "Введите год")
        bot.register_next_step_handler(msg, year_input)
    if (message.text == "Выборы"):
        ### Проверка пуста ли таблица vote, если не пуста, то сообщить (спросить перезаписать)
        voting.voting()
        print("Выборы проведены")
    if (message.text == "Запись \n результатов"):
        ###Проверка есть ли в history уже данные этой ротации
        if db.check_current_vote_in_history() == False:
            db.insert_voting_results_into_history()
            msg = bot.send_message(message.chat.id, "Данные записаны!")
            bot.register_next_step_handler(msg, user_handler)
        else:
            msg = bot.send_message(message.chat.id, "Данные уже есть в таблице!")   #### Сделаьб вопрос перезаписать или нет
            bot.register_next_step_handler(msg, user_handler)
    if (message.text == "Подмена"):
        print("Подмена")

def year_input(message):
    global year
    year = message.text
    msg = bot.send_message(message.chat.id, "Введите месяц")
    bot.register_next_step_handler(msg, month_input)

def month_input (message):
    global month
    month = message.text
    db.update_period(year, month)




bot.infinity_polling(none_stop=True)